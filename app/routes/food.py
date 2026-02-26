from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.food import (
    PetFoodItemResponse, FeedPetRequest, FeedPetResponse,
    MealLogCreate, MealLogResponse, CoinsResponse
)
from app.services import food_service
from app.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/api/food",
    tags=["Food & Nutrition"]
)


# ── Coins ──────────────────────────────────────────────────────────────────────

@router.get("/coins", response_model=CoinsResponse)
async def get_coins(current_user: User = Depends(get_current_user)):
    """Get the current user's coin balance."""
    return {"coins": current_user.coins or 0}


# ── Pet food shop ──────────────────────────────────────────────────────────────

@router.get("/shop", response_model=list[PetFoodItemResponse])
async def get_shop(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all available pet food items from the shop.
    Each item has a coin price and a stat effect on your pet.
    """
    return food_service.get_shop_items(db)


@router.post("/shop/feed", response_model=FeedPetResponse)
async def feed_pet(
    feed_data: FeedPetRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Buy a pet food item and feed it to your pet.

    - Deducts coins from your balance.
    - Boosts the corresponding pet stat (health, happiness, or energy).
    - Returns 400 if you don't have enough coins.
    - Returns 404 if the item doesn't exist.
    """
    result = food_service.feed_pet(db, current_user, feed_data.item_id)
    return result


# ── Meal logging ───────────────────────────────────────────────────────────────

@router.post("/meal", response_model=MealLogResponse, status_code=201)
async def log_meal(
    meal_data: MealLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Log a meal you ate today.

    - **meal_type**: breakfast / lunch / dinner / snack
    - **quality**: healthy / okay / junk

    Meal quality affects your pet:
    - healthy → +8 health, +3 happiness
    - okay    → +2 health, +1 happiness
    - junk    → -5 health, +5 happiness
    """
    return food_service.log_meal(db, current_user, meal_data)


@router.get("/meal/history", response_model=list[MealLogResponse])
async def get_meal_history(
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get your recent meal logs, newest first."""
    return food_service.get_meal_history(db, current_user.id, limit=limit)
