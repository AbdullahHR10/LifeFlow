"""Module that contains the Habit class."""
from .base_model import BaseModel
from sqlalchemy import (Column, String, Integer, Date, Boolean,
                        ForeignKey, Enum as SqlEnum)
from sqlalchemy.orm import relationship
from ..utils.enums import BackgroundColor, Priority, Category, Frequency


class Habit(BaseModel):
    """Represents a habit in the application."""
    __tablename__ = "habits"

    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    frequency = Column(SqlEnum(Frequency, name="frequency_enum"),
                       nullable=False)
    target_count = Column(Integer, nullable=False)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_completed = Column(Date, nullable=True)
    priority = Column(SqlEnum(Priority, name="priority_enum"), nullable=False)
    category = Column(SqlEnum(Category, name="category_enum"), nullable=False)
    is_active = Column(Boolean, default=True)
    background_color = Column(SqlEnum(BackgroundColor), nullable=True)

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="habits")
