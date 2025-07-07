"""Module that contains the Habit class."""
from .base_model import BaseModel
from sqlalchemy import (Column, String, Integer, Date, Boolean, Text,
                        ForeignKey, Enum as SqlEnum)
from sqlalchemy.orm import relationship, validates
from ..utils.enums import BackgroundColor, Priority, Category, Frequency
from ..utils.validators import validate_string_field
from datetime import date, timedelta


class Habit(BaseModel):
    """Represents a habit in the application."""
    __tablename__ = "habits"

    title = Column(String(30), nullable=False)
    description = Column(Text, nullable=True)
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

    @validates("title")
    def validate_title(self, key: str, value: str) -> str:
        """
        Validates the task's title.

        Parameters:
            key (str): The name of the field being validated.
            value (str): The name to validate.

        Returns:
            str: The validated name value.

        Raises:
            ValueError: If the name is not between 3 and 30 characters.
        """
        validate_string_field(
            key=key,
            value=value,
            min_length=3,
            max_length=30
        )
        return value

    def mark_complete(self) -> None:
        """Marks the habit as completed for today."""
        today = date.today()
        if self.last_completed == today:
            raise ValueError("Habit already completed today.")
        yesterday = today - timedelta(days=1)
        if self.last_completed == yesterday:
            self.current_streak += 1
        else:
            self.current_streak = 1

        self.last_completed = today

        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

        self.save()
