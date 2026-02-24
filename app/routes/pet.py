from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.models.pet import Pet
from app.schemas.pet import PetCreate, PetResponse
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
    Create a new pet for the current user.

    Each user can only have one pet. If they already have one, this will fail.
    """
    # Check if user already has a pet
    existing_pet = db.query(Pet).filter(Pet.user_id == current_user.id).first()

    if existing_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a pet"
        )

    # Create new pet
    new_pet = Pet(
        user_id=current_user.id,
        name=pet_data.name,
        species=pet_data.species or "egg"
    )

    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)

    return new_pet

@router.get("/my-pet", response_model=PetResponse)
async def get_my_pet(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's pet"""
    pet = db.query(Pet).filter(Pet.user_id == current_user.id).first()

    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )

    return pet

@router.get("/{pet_id}", response_model=PetResponse)
async def get_pet(
    pet_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific pet (only if it belongs to current user)"""
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )

    if pet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this pet"
        )

    return pet
