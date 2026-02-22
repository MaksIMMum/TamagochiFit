from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Pet(Base):
    __tablename__ = "pets"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # 1-to-1 relationship with the user
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Pet characteristics
    name = Column(String(50), nullable=False)
    species = Column(String(50), default="egg")

    # Progress
    level = Column(Integer, default=1)
    xp = Column(Float, default=0.0)  # Experience gained through workouts

    # Vital stats
    health = Column(Float, default=100.0)
    happiness = Column(Float, default=100.0)
    energy = Column(Float, default=100.0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Last interaction time
    last_interacted = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # ORM Relationship
    owner = relationship("User", back_populates="pet")

    def __repr__(self):
        return f"<Pet {self.name} (Lvl {self.level})>"
