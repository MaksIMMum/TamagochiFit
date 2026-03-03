from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.workout import SplitFinishRequest, SplitFinishResponse
from app.services import pet_service
from app.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/api/splits",
    tags=["Splits"]
)

@router.post("/finish", response_model=SplitFinishResponse, status_code=status.HTTP_200_OK)
async def finish_split(
    split_data: SplitFinishRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Process a completed workout split.
    Adds coins to the user account and awards XP/stat changes to their pet.
    """
    # 1. Update user coins
    current_user.coins += split_data.coins_earned

    new_xp = 0.0
    pet_level = 0

    # 2. Update pet XP and stats (if the user has a pet)
    try:
        # Fetch the pet
        pet = pet_service.get_pet_by_user_id(db, current_user.id)

        # Award XP (this internally handles the check_level_up logic and commits)
        pet = pet_service.award_xp(db, current_user.id, split_data.xp_earned)

        # Update physical stats (workouts increase health/happiness but cost energy)
        pet = pet_service.update_pet_stats(
            db,
            current_user.id,
            health_delta=5.0,
            happiness_delta=10.0,
            energy_delta=-15.0
        )

        new_xp = pet.xp
        pet_level = pet.level
    except HTTPException:
        # Fails gracefully if no pet exists for the user yet
        pass

    # 3. Commit the user coin updates to the database
    db.commit()
    db.refresh(current_user)

    return SplitFinishResponse(
        message=f"Successfully finished {split_data.split_name}!",
        new_coins_total=current_user.coins,
        new_xp_total=new_xp,
        pet_level=pet_level
    )
