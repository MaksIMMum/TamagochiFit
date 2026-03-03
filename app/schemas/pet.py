from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Request Schemas
class PetCreate(BaseModel):
    """Schema for creating a pet"""
    name: str = Field(..., min_length=1, max_length=50)
    pet_type: str = Field(default="blue", max_length=50)
    species: Optional[str] = Field("egg", max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Felix",
                "pet_type": "blue",
                "species": "egg"
            }
        }

# Response Schemas
class PetResponse(BaseModel):
    """Schema for pet response"""
    id: int
    user_id: int
    name: str
    pet_type: str
    species: str
    level: int
    xp: float
    health: float
    happiness: float
    energy: float
    created_at: datetime
    last_interacted: datetime

    class Config:
        from_attributes = True
