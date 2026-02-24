from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from app.services.user_service import UserService
from app.services.security import create_access_token, create_refresh_token
from app.utils.dependencies import get_current_user
from app.models import User
from config import settings

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user.

    - **username**: Must be 3-50 characters
    - **email**: Valid email address
    - **password**: Must be at least 8 characters
    - **full_name**: Optional
    """
    new_user = UserService.create_user(db, user_data)
    return new_user

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login and receive JWT tokens.

    Returns:
    - **access_token**: JWT token for authenticated requests (expires in 30 min)
    - **refresh_token**: Token to get new access token without re-login (expires in 7 days)
    - **token_type**: Always "bearer"
    - **expires_in**: Seconds until access token expires
    """
    # Authenticate user
    user = UserService.authenticate_user(
        db,
        login_data.username,
        login_data.password
    )

    # Create tokens
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token_data: dict,
    db: Session = Depends(get_db)
):
    """
    Get a new access token using refresh token.

    Body:
    - **refresh_token**: The refresh token from login
    """
    from app.services.security import verify_token
    from jose import JWTError

    refresh_token = refresh_token_data.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token required"
        )

    try:
        payload = verify_token(refresh_token)
        user_id = payload.get("sub")

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # Verify user still exists and is active
    user = UserService.get_user_by_id(db, user_id)

    # Create new access token
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    new_access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user's information.

    Requires: Authorization header with Bearer token
    """
    return current_user

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout user (client-side: delete tokens).

    Note: JWT tokens are stateless, so logout is handled on the client side
    by deleting the stored tokens. This endpoint is here for consistency.
    """
    return {"message": "Successfully logged out"}
