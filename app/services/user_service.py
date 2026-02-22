from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import User
from app.schemas import UserRegister, UserLogin
from app.services.security import hash_password, verify_password
from datetime import datetime, timezone
from fastapi import HTTPException, status

class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserRegister) -> User:
        """Create a new user."""
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.username == user_data.username) |
            (User.email == user_data.email)
        ).first()

        if existing_user:
            if existing_user.username == user_data.username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

        # Create user
        hashed_password = hash_password(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        """Authenticate user with username and password."""
        # Find user by username (can also search by email)
        user = db.query(User).filter(User.username == username).first()

        if not user:
            # Try email as well
            user = db.query(User).filter(User.email == username).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled"
            )

        # Update last login
        user.last_login = datetime.now(timezone.utc)
        db.commit()

        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Get user by ID."""
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """Get user by username."""
        user = db.query(User).filter(User.username == username).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user
