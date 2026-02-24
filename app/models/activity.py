from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Activity(Base):
    __tablename__ = "activities"

    # Primary identifier
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key linking to the User (One-to-Many relationship)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Activity details
    activity_type = Column(String(50), nullable=False) # e.g., "strength", "cardio", "nutrition"
    name = Column(String(100), nullable=False)         # e.g., "Calf raises in Smith machine", "Running"
    duration_minutes = Column(Integer, nullable=False, default=0)

    # Gamification and health metrics
    calories_burned = Column(Integer, default=0)
    xp_earned = Column(Float, default=0.0)             # How much XP this activity gave to the Pet

    # Timestamp of when the activity was logged
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ORM Relationship
    user = relationship("User", back_populates="activities")

    def __repr__(self):
        return f"<Activity {self.name} ({self.duration_minutes} min, +{self.xp_earned} XP)>"
