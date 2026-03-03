from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.config.pet_types import PET_TYPES, get_all_pet_types

router = APIRouter(
    prefix="/api/pet-types",
    tags=["Pet Types"]
)

@router.get("/")
async def list_pet_types(db: Session = Depends(get_db)):
    """
    Get all available pet types with their evolution chains.
    Returns: List of pet types with id, name, emoji, preview_image
    """
    return get_all_pet_types()

@router.get("/{pet_type_id}")
async def get_pet_type_detail(pet_type_id: str, db: Session = Depends(get_db)):
    """
    Get complete evolution chain for a specific pet type.
    Returns: Pet type with full evolution_chain data
    """
    if pet_type_id not in PET_TYPES:
        return {"error": f"Pet type '{pet_type_id}' not found"}

    pet_type = PET_TYPES[pet_type_id]
    return {
        "id": pet_type_id,
        "name": pet_type["name"],
        "emoji": pet_type["emoji"],
        "evolution_chain": pet_type["evolution_chain"]
    }
