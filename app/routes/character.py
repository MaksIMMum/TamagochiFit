from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.pet import PetCreate, PetResponse
from app.services import pet_service
from app.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/api/pet",
    tags=["Pet"]
)


@router.post("/create", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
async def create_pet(
    pet_data: PetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a pet for the currently logged-in user.

    - Called at the end of the hatch flow after the user names their pet.
    - Returns 400 if the user already has a pet.
    """
    return pet_service.create_pet(db, current_user.id, pet_data)


@router.get("/me", response_model=PetResponse)
async def get_my_pet(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current user's pet.

    - Automatically applies stat decay based on time since last interaction.
    - Automatically triggers a level-up if XP threshold is reached.
    - Returns 404 if the user hasn't created a pet yet.
    """
    return pet_service.get_pet_by_user_id(db, current_user.id)
