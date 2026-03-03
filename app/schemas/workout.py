from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class WorkoutLogCreate(BaseModel):
    """Schema for logging a workout."""
    exercise_name:   str   = Field(..., min_length=1, max_length=100)
    muscle_group:    Optional[str]   = Field(None, max_length=50)
    duration_mins:   float = Field(..., gt=0)
    sets:            Optional[int]   = Field(None, gt=0)
    reps:            Optional[int]   = Field(None, gt=0)
    calories_burned: Optional[float] = Field(None, gt=0)
    notes:           Optional[str]   = None
    logged_at:       Optional[datetime] = None  # if omitted, server uses now()

    class Config:
        json_schema_extra = {
            "example": {
                "exercise_name": "Bench Press",
                "muscle_group": "chest",
                "duration_mins": 45,
                "sets": 4,
                "reps": 10,
                "calories_burned": 300,
                "notes": "Felt strong today"
            }
        }


class WorkoutLogResponse(BaseModel):
    """Schema for a single workout log entry."""
    id:              int
    user_id:         int
    exercise_name:   str
    muscle_group:    Optional[str]   = None
    duration_mins:   float
    sets:            Optional[int]   = None
    reps:            Optional[int]   = None
    calories_burned: Optional[float] = None
    notes:           Optional[str]   = None
    logged_at:       datetime

    class Config:
        from_attributes = True


class WorkoutLogWithXP(WorkoutLogResponse):
    """Workout log response that also reports XP awarded to pet."""
    xp_awarded: float
    pet_level:  int


class StreakResponse(BaseModel):
    """Current workout streak for the user."""
    current_streak: int   # consecutive days with at least one workout
    longest_streak: int
class SplitFinishRequest(BaseModel):
    """Payload sent from the frontend when a split is finished."""
    duration_mins: float
    coins_earned: int
    xp_earned: float
    split_name: str = "Workout Split"

class SplitFinishResponse(BaseModel):
    """Response returned after processing a finished split."""
    message: str
    new_coins_total: int
    new_xp_total: float
    pet_level: int
