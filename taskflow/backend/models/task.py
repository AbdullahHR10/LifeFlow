"""Module that contains the Task class."""
from .base_model import BaseModel
from sqlalchemy import (Column,
                        String, Text, Date, DateTime, Boolean,
                        Enum as SqlEnum, ForeignKey)
from sqlalchemy.orm import relationship, validates
from datetime import datetime
from ..utils.enums import Priority, Category
from ..utils.validators import validate_string_field


class Task(BaseModel):
    """Represents a task in the application."""
    __tablename__ = "tasks"
    title = Column(String(30), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(SqlEnum(Priority, name="priority_enum"), nullable=False)
    deadline = Column(Date, nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
    category = Column(SqlEnum(Category, name="category_enum"), nullable=False)
    completed_at = Column(DateTime, nullable=True)

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="tasks")

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
        """Marks the task as completed."""
        self.completed = True
        self.completed_at = datetime.now()
        self.save()

    def mark_incomplete(self) -> None:
        """Marks the task as incomplete."""
        self.completed = False
        self.completed_at = None
        self.save()
