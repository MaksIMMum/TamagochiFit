from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.models.pet import Pet
from app.schemas.pet import PetCreate


# ── XP / levelling ────────────────────────────────────────────────────────────

def _xp_for_next_level(level: int) -> float:
    """XP needed to reach the next level (level * 100)."""
    return level * 100.0


LEVEL_SPECIES: dict[int, str] = {
    1:  "egg",
    2:  "cracked_egg",
    3:  "chick",
    5:  "kitten",
    8:  "cat",
    12: "cool_cat",
}

def _species_for_level(level: int) -> str:
    """Return the species string for a given level."""
    species = "egg"
    for threshold, name in sorted(LEVEL_SPECIES.items()):
        if level >= threshold:
            species = name
    return species


def check_level_up(pet: Pet) -> None:
    """Increment level (and update species) while XP exceeds the threshold."""
    while pet.xp >= _xp_for_next_level(pet.level):
        pet.xp -= _xp_for_next_level(pet.level)
        pet.level += 1
    pet.species = _species_for_level(pet.level)


# ── Stat decay ────────────────────────────────────────────────────────────────

# How many points each stat loses per hour of inactivity
DECAY_PER_HOUR = {
    "health":    2.0,
    "happiness": 3.0,
    "energy":    2.5,
}

def apply_decay(pet: Pet) -> None:
    """Reduce pet stats based on time elapsed since last_interacted."""
    now = datetime.now(timezone.utc)

    last = pet.last_interacted
    if last.tzinfo is None:
        last = last.replace(tzinfo=timezone.utc)

    hours_elapsed = (now - last).total_seconds() / 3600.0

    if hours_elapsed < 0.05:   # less than ~3 minutes — skip
        return

    for stat, rate in DECAY_PER_HOUR.items():
        current = getattr(pet, stat)
        new_val = max(0.0, current - rate * hours_elapsed)
        setattr(pet, stat, round(new_val, 2))

    pet.last_interacted = now


# ── CRUD ──────────────────────────────────────────────────────────────────────

def create_pet(db: Session, user_id: int, pet_data: PetCreate) -> Pet:
    """Create a new pet for a user. Raises 400 if the user already has one."""
    existing = db.query(Pet).filter(Pet.user_id == user_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a pet"
        )

    pet = Pet(
        user_id=user_id,
        name=pet_data.name,
        species=_species_for_level(1),
    )
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


def get_pet_by_user_id(db: Session, user_id: int) -> Pet:
    """
    Fetch the pet, apply stat decay, persist the updated stats, and return it.
    Raises 404 if the user has no pet yet.
    """
    pet = db.query(Pet).filter(Pet.user_id == user_id).first()
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pet found for this user"
        )

    apply_decay(pet)
    check_level_up(pet)
    db.commit()
    db.refresh(pet)
    return pet


def award_xp(db: Session, user_id: int, xp_amount: float) -> Pet:
    """Award XP to a user's pet and trigger a level-up check."""
    pet = db.query(Pet).filter(Pet.user_id == user_id).first()
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pet found for this user"
        )

    pet.xp += xp_amount
    pet.last_interacted = datetime.now(timezone.utc)
    check_level_up(pet)
    db.commit()
    db.refresh(pet)
    return pet


def update_pet_stats(
    db: Session,
    user_id: int,
    *,
    health_delta: float = 0.0,
    happiness_delta: float = 0.0,
    energy_delta: float = 0.0,
) -> Pet:
    """
    Add (or subtract) from individual pet stats, clamped to [0, 100].
    Also updates last_interacted so decay resets.
    """
    pet = db.query(Pet).filter(Pet.user_id == user_id).first()
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pet found for this user"
        )

    pet.health    = round(max(0.0, min(100.0, pet.health    + health_delta)),    2)
    pet.happiness = round(max(0.0, min(100.0, pet.happiness + happiness_delta)), 2)
    pet.energy    = round(max(0.0, min(100.0, pet.energy    + energy_delta)),    2)
    pet.last_interacted = datetime.now(timezone.utc)

    db.commit()
    db.refresh(pet)
    return pet
