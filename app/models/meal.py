from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class MealLog(Base):
    """Records a meal logged by the user."""
    __tablename__ = "meal_logs"

    id        = Column(Integer, primary_key=True, index=True)
    user_id   = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    meal_type = Column(String(20), nullable=False)   # "breakfast", "lunch", "dinner", "snack"
    quality   = Column(String(10), nullable=False)   # "healthy", "okay", "junk"
    notes     = Column(String(200), nullable=True)
    logged_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="meal_logs")

    def __repr__(self):
        return f"<MealLog {self.meal_type} ({self.quality}) user={self.user_id}>"
