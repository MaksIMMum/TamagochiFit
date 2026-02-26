from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class PetFoodItem(Base):
    """Items available in the pet food shop."""
    __tablename__ = "pet_food_items"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    price       = Column(Integer, nullable=False)          # cost in coins
    effect_stat = Column(String(20), nullable=False)       # "health", "happiness", or "energy"
    effect_value = Column(Float, nullable=False)           # how much the stat increases

    feeding_logs = relationship("FeedingLog", back_populates="item")

    def __repr__(self):
        return f"<PetFoodItem {self.name} (+{self.effect_value} {self.effect_stat})>"


class FeedingLog(Base):
    """Records each time a user feeds their pet."""
    __tablename__ = "feeding_logs"

    id      = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("pet_food_items.id"), nullable=False)
    fed_at  = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="feeding_logs")
    item = relationship("PetFoodItem", back_populates="feeding_logs")

    def __repr__(self):
        return f"<FeedingLog user={self.user_id} item={self.item_id}>"
