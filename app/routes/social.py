from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.pet import Pet
from app.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/api/social",
    tags=["Social"]
)



class LeaderboardEntry(BaseModel):
    rank:       int
    username:   str
    full_name:  Optional[str] = None
    pet_name:   str
    pet_species: str
    pet_level:  int
    xp:         float
    is_current_user: bool  # highlights the requesting user's row

    class Config:
        from_attributes = True


class LeaderboardResponse(BaseModel):
    entries:      list[LeaderboardEntry]
    current_user_rank: Optional[int] = None



@router.get("/leaderboard", response_model=LeaderboardResponse)
async def get_leaderboard(
    limit: int = Query(10, ge=1, le=50, description="Number of top users to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the top users ranked by their pet's XP.

    - Returns up to 50 entries (default 10).
    - Marks the requesting user's row with `is_current_user: true`.
    - Also returns `current_user_rank` even if they fall outside the top N.
    """
    # Join users with their pets and rank by XP descending
    results = (
        db.query(User, Pet)
        .join(Pet, Pet.user_id == User.id)
        .filter(User.is_active == True)
        .order_by(desc(Pet.xp), desc(Pet.level))
        .limit(limit)
        .all()
    )

    entries = []
    current_user_rank = None

    for rank, (user, pet) in enumerate(results, start=1):
        is_me = user.id == current_user.id
        if is_me:
            current_user_rank = rank

        entries.append(LeaderboardEntry(
            rank=rank,
            username=user.username,
            full_name=user.full_name,
            pet_name=pet.name,
            pet_species=pet.species,
            pet_level=pet.level,
            xp=pet.xp,
            is_current_user=is_me,
        ))

    # If current user isn't in the top N, find their actual rank
    if current_user_rank is None:
        rank_result = (
            db.query(User, Pet)
            .join(Pet, Pet.user_id == User.id)
            .filter(User.is_active == True)
            .order_by(desc(Pet.xp), desc(Pet.level))
            .all()
        )
        for rank, (user, pet) in enumerate(rank_result, start=1):
            if user.id == current_user.id:
                current_user_rank = rank
                break

    return LeaderboardResponse(
        entries=entries,
        current_user_rank=current_user_rank
    )
