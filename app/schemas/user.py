from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# Request Schemas
class UserRegister(BaseModel):
    """Schema for user registration"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: Optional[str] = Field(None, max_length=200)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "SecurePass123!",
                "full_name": "John Doe"
            }
        }

class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "SecurePass123!"
            }
        }

# Response Schemas
class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int  # seconds

class UserResponse(BaseModel):
    """Schema for user response (no password)"""
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserDetailResponse(UserResponse):
    """Extended user response with additional fields"""
    is_verified: bool
    last_login: Optional[datetime] = None
