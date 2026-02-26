from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.models.food import PetFoodItem, FeedingLog
from app.models.meal import MealLog
from app.models.user import User
from app.schemas.food import MealLogCreate
from app.services import pet_service


# ── Meal quality → pet stat effects ───────────────────────────────────────────

MEAL_EFFECTS = {
    "healthy": {"health_delta": +8.0,  "happiness_delta": +3.0},
    "okay":    {"health_delta": +2.0,  "happiness_delta": +1.0},
    "junk":    {"health_delta": -5.0,  "happiness_delta": +5.0},  # tasty but bad for health
}

MEAL_EFFECT_DESCRIPTIONS = {
    "healthy": "Your pet feels great! (+8 health, +3 happiness)",
    "okay":    "Your pet is doing fine. (+2 health, +1 happiness)",
    "junk":    "Your pet enjoyed the treat but feels a bit off. (-5 health, +5 happiness)",
}


# ── Coin helpers ───────────────────────────────────────────────────────────────

def award_coins(db: Session, user: User, amount: int) -> None:
    """Add coins to a user's balance."""
    user.coins = (user.coins or 0) + amount
    db.commit()


def spend_coins(db: Session, user: User, amount: int) -> None:
    """Deduct coins from a user's balance. Raises 400 if insufficient."""
    if (user.coins or 0) < amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not enough coins. You have {user.coins}, need {amount}."
        )
    user.coins -= amount
    db.commit()


# ── Pet food shop ──────────────────────────────────────────────────────────────

def get_shop_items(db: Session) -> list[PetFoodItem]:
    """Return all available pet food items."""
    return db.query(PetFoodItem).all()


def feed_pet(db: Session, user: User, item_id: int) -> dict:
    """
    Buy a pet food item and feed it to the user's pet.
    Deducts coins, applies stat boost, logs the feeding.
    """
    item = db.query(PetFoodItem).filter(PetFoodItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet food item not found"
        )

    # Deduct coins (raises 400 if insufficient)
    spend_coins(db, user, item.price)

    # Apply stat boost to pet
    kwargs = {f"{item.effect_stat}_delta": item.effect_value}
    pet = pet_service.update_pet_stats(db, user.id, **kwargs)

    # Log the feeding
    log = FeedingLog(user_id=user.id, item_id=item.id)
    db.add(log)
    db.commit()

    # Get updated stat value
    stat_after = getattr(pet, item.effect_stat)

    return {
        "message": f"You fed {item.name} to your pet!",
        "item_name": item.name,
        "effect_stat": item.effect_stat,
        "effect_value": item.effect_value,
        "coins_spent": item.price,
        "coins_remaining": user.coins,
        "pet_stat_after": stat_after,
    }


# ── Meal logging ───────────────────────────────────────────────────────────────

def log_meal(db: Session, user: User, meal_data: MealLogCreate) -> MealLog:
    """
    Log a human meal and apply the corresponding effect to the user's pet.
    """
    log = MealLog(
        user_id=user.id,
        meal_type=meal_data.meal_type.value,
        quality=meal_data.quality.value,
        notes=meal_data.notes,
        logged_at=meal_data.logged_at or datetime.now(timezone.utc)
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    # Apply pet effect (silently skip if no pet yet)
    try:
        effects = MEAL_EFFECTS[meal_data.quality.value]
        pet_service.update_pet_stats(db, user.id, **effects)
    except Exception:
        pass

    # Attach human-readable effect description for the response
    log.pet_effect = MEAL_EFFECT_DESCRIPTIONS[meal_data.quality.value]
    return log


def get_meal_history(db: Session, user_id: int, limit: int = 50) -> list[MealLog]:
    """Return recent meal logs for a user, newest first."""
    return (
        db.query(MealLog)
        .filter(MealLog.user_id == user_id)
        .order_by(MealLog.logged_at.desc())
        .limit(limit)
        .all()
    )


# ── Shop seeding ───────────────────────────────────────────────────────────────

INITIAL_SHOP_ITEMS = [
    {"name": "Apple",        "description": "A fresh apple. Simple and healthy.",         "price": 5,  "effect_stat": "health",    "effect_value": 10.0},
    {"name": "Fish",         "description": "Your pet loves fish!",                        "price": 10, "effect_stat": "happiness", "effect_value": 15.0},
    {"name": "Energy Drink", "description": "Gives your pet a burst of energy.",           "price": 8,  "effect_stat": "energy",    "effect_value": 20.0},
    {"name": "Salad",        "description": "Nutritious greens for a healthy pet.",        "price": 7,  "effect_stat": "health",    "effect_value": 15.0},
    {"name": "Cake",         "description": "A treat! Great for happiness, not health.",   "price": 15, "effect_stat": "happiness", "effect_value": 25.0},
    {"name": "Steak",        "description": "Premium meal. Big health and energy boost.",  "price": 25, "effect_stat": "health",    "effect_value": 30.0},
]

def seed_shop(db: Session) -> None:
    """Populate the pet food shop with default items if empty."""
    if db.query(PetFoodItem).count() == 0:
        for item_data in INITIAL_SHOP_ITEMS:
            db.add(PetFoodItem(**item_data))
        db.commit()
