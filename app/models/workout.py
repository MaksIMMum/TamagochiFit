from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    exercise_name  = Column(String(100), nullable=False)
    muscle_group   = Column(String(50), nullable=True)
    duration_mins  = Column(Float, nullable=False)
    sets           = Column(Integer, nullable=True)
    reps           = Column(Integer, nullable=True)
    calories_burned = Column(Float, nullable=True)
    notes          = Column(Text, nullable=True)

    logged_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="workout_logs")

    def __repr__(self):
        return f"<WorkoutLog {self.exercise_name} ({self.duration_mins} mins) by user {self.user_id}>"
