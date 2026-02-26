from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import datetime, timezone, timedelta

from app.models.workout import WorkoutLog
from app.schemas.workout import WorkoutLogCreate
from app.services import pet_service



def _calculate_xp(workout: WorkoutLogCreate) -> float:
    """
    Award XP based on workout duration and intensity.
    Base: 1 XP per minute. Bonus for sets/reps and calories.
    """
    xp = workout.duration_mins * 1.0

    if workout.sets and workout.reps:
        xp += (workout.sets * workout.reps) * 0.1

    if workout.calories_burned:
        xp += workout.calories_burned * 0.05

    return round(xp, 2)



def log_workout(db: Session, user_id: int, workout_data: WorkoutLogCreate) -> tuple[WorkoutLog, float]:
    """
    Save a workout log and reward the user's pet with XP and stat boosts.
    Returns the saved log and the XP awarded.
    """
    log = WorkoutLog(
        user_id=user_id,
        exercise_name=workout_data.exercise_name,
        muscle_group=workout_data.muscle_group,
        duration_mins=workout_data.duration_mins,
        sets=workout_data.sets,
        reps=workout_data.reps,
        calories_burned=workout_data.calories_burned,
        notes=workout_data.notes,
        logged_at=workout_data.logged_at or datetime.now(timezone.utc)
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    xp_awarded = _calculate_xp(workout_data)
    try:
        pet_service.award_xp(db, user_id, xp_awarded)
        coins_earned = max(1, int(xp_awarded / 10))
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            food_service.award_coins(db, user, coins_earned)

        pet_service.update_pet_stats(
            db, user_id,
            happiness_delta=+10.0,
            energy_delta=-5.0,
            health_delta=+5.0,
        )
    except Exception:
        pass

    return log, xp_awarded


def get_workout_history(
    db: Session,
    user_id: int,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    limit: int = 50,
) -> list[WorkoutLog]:
    """Return workout logs for a user, newest first, with optional date range."""
    query = db.query(WorkoutLog).filter(WorkoutLog.user_id == user_id)

    if start_date:
        query = query.filter(WorkoutLog.logged_at >= start_date)
    if end_date:
        query = query.filter(WorkoutLog.logged_at <= end_date)

    return query.order_by(WorkoutLog.logged_at.desc()).limit(limit).all()



def get_streak(db: Session, user_id: int) -> dict:
    """
    Calculate the user's current and longest workout streaks.
    A streak is a consecutive sequence of calendar days with at least one log.
    """
    # Get all distinct workout dates for the user, newest first
    rows = (
        db.query(cast(WorkoutLog.logged_at, Date).label("day"))
        .filter(WorkoutLog.user_id == user_id)
        .group_by(cast(WorkoutLog.logged_at, Date))
        .order_by(cast(WorkoutLog.logged_at, Date).desc())
        .all()
    )

    if not rows:
        return {"current_streak": 0, "longest_streak": 0}

    dates = [row.day for row in rows]
    today = datetime.now(timezone.utc).date()

    # Current streak — count consecutive days backwards from today (or yesterday)
    current_streak = 0
    check = today
    for date in dates:
        if date == check or date == check - timedelta(days=1):
            current_streak += 1
            check = date - timedelta(days=1)  # expect next date to be one day earlier
        else:
            break

    longest_streak = 1
    running = 1
    for i in range(1, len(dates)):
        if (dates[i - 1] - dates[i]).days == 1:
            running += 1
            longest_streak = max(longest_streak, running)
        else:
            running = 1

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak
    }
