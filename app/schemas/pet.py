from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PetCreate(BaseModel):
    """Schema for creating a new pet."""
    name: str = Field(..., min_length=1, max_length=50)

    class Config:
        json_schema_extra = {
            "example": {"name": "Felix"}
        }


class PetResponse(BaseModel):
    """Schema returned for all pet endpoints."""
    id: int
    user_id: int
    name: str
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
