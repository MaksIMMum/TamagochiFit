from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.schemas.workout import WorkoutLogCreate, WorkoutLogWithXP, WorkoutLogResponse, StreakResponse
from app.services import workout_service
from app.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/api/workout",
    tags=["Workout"]
)


@router.post("/log", response_model=WorkoutLogWithXP, status_code=201)
async def log_workout(
    workout_data: WorkoutLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Log a completed workout.

    - Awards XP to the user's pet based on duration, sets/reps, and calories.
    - Boosts pet happiness (+10) and health (+5), costs energy (-5).
    - Returns the saved log plus how much XP was awarded and the pet's current level.
    """
    log, xp_awarded = workout_service.log_workout(db, current_user.id, workout_data)

    # Fetch current pet level to include in response (optional — skip if no pet)
    pet_level = 1
    try:
        from app.services import pet_service
        pet = pet_service.get_pet_by_user_id(db, current_user.id)
        pet_level = pet.level
    except Exception:
        pass

    return WorkoutLogWithXP(
        **WorkoutLogResponse.model_validate(log).model_dump(),
        xp_awarded=xp_awarded,
        pet_level=pet_level,
    )


@router.get("/history", response_model=list[WorkoutLogResponse])
async def get_history(
    start_date: Optional[datetime] = Query(None, description="Filter from this date (ISO 8601)"),
    end_date:   Optional[datetime] = Query(None, description="Filter to this date (ISO 8601)"),
    limit:      int                = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get workout history for the current user, newest first.

    Optional filters:
    - **start_date** — only return logs on or after this date
    - **end_date** — only return logs on or before this date
    - **limit** — max number of results (default 50, max 200)
    """
    return workout_service.get_workout_history(
        db, current_user.id,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )


@router.get("/streak", response_model=StreakResponse)
async def get_streak(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current user's workout streak.

    - **current_streak** — consecutive days with at least one workout up to today
    - **longest_streak** — all-time best streak
    """
    return workout_service.get_streak(db, current_user.id)
