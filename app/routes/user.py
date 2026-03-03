from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.utils.dependencies import get_current_user
from app.services.security import hash_password, verify_password

router = APIRouter(
    prefix="/api/user",
    tags=["User Profile"]
)


class UserUpdateRequest(BaseModel):
    """Schema for updating user profile"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=200)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "newusername",
                "full_name": "New Full Name"
            }
        }


class PasswordChangeRequest(BaseModel):
    """Schema for changing password"""
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "OldPass123!",
                "new_password": "NewPass456!"
            }
        }


@router.patch("/me", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile information.

    - **username**: New username (must be unique, 3-50 chars)
    - **full_name**: New full name (max 200 chars)

    Only provided fields will be updated.
    """
    if update_data.username is not None:
        if update_data.username != current_user.username:
            existing_user = db.query(User).filter(
                User.username == update_data.username
            ).first()

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
            current_user.username = update_data.username

    if update_data.full_name is not None:
        current_user.full_name = update_data.full_name

    db.commit()
    db.refresh(current_user)

    return current_user


@router.patch("/me/password")
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change current user's password.

    - **current_password**: User's current password for verification
    - **new_password**: New password (min 8 characters)
    """
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    current_user.hashed_password = hash_password(password_data.new_password)

    db.commit()

    return {"message": "Password successfully changed"}
