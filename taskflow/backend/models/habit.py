"""Module that contains the Note class."""
from .base_model import BaseModel
from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Habit(BaseModel):
    """Represents a note in the application."""
    __tablename__ = "habits"

    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    frequency = Column(String(50), nullable=False)
    target_count = Column(Integer, nullable=False)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_completed = Column(Date, nullable=True)
    priority = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    color = Column(String(7), nullable=False)
    is_active = Column(Boolean, default=True)

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="habits")
