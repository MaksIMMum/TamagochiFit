from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum



class MealType(str, Enum):
    breakfast = "breakfast"
    lunch     = "lunch"
    dinner    = "dinner"
    snack     = "snack"

class MealQuality(str, Enum):
    healthy = "healthy"
    okay    = "okay"
    junk    = "junk"


# ── Pet food shop ──────────────────────────────────────────────────────────────

class PetFoodItemResponse(BaseModel):
    id:           int
    name:         str
    description:  Optional[str] = None
    price:        int
    effect_stat:  str
    effect_value: float

    class Config:
        from_attributes = True


class FeedPetRequest(BaseModel):
    item_id: int = Field(..., description="ID of the shop item to feed to the pet")


class FeedPetResponse(BaseModel):
    message:      str
    item_name:    str
    effect_stat:  str
    effect_value: float
    coins_spent:  int
    coins_remaining: int
    pet_stat_after: float   # the pet's stat value after feeding


# ── Meal logging ───────────────────────────────────────────────────────────────

class MealLogCreate(BaseModel):
    meal_type: MealType
    quality:   MealQuality
    notes:     Optional[str] = Field(None, max_length=200)
    logged_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "meal_type": "lunch",
                "quality": "healthy",
                "notes": "Big salad with chicken"
            }
        }


class MealLogResponse(BaseModel):
    id:        int
    user_id:   int
    meal_type: str
    quality:   str
    notes:     Optional[str] = None
    logged_at: datetime
    pet_effect: Optional[str] = None   # human-readable description of effect on pet

    class Config:
        from_attributes = True


# ── Coins ──────────────────────────────────────────────────────────────────────

class CoinsResponse(BaseModel):
    coins: int
