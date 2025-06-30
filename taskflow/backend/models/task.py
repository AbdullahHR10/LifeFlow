"""Module that contains the Task class."""
from .base_model import BaseModel
from sqlalchemy import (Column,
                        String, Text, Date, DateTime, Boolean,
                        Enum as SqlEnum, ForeignKey)
from sqlalchemy.orm import relationship
from datetime import datetime
from ..utils.enums import Priority, Category


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

    def mark_complete(self):
        """Marks the task as completed."""
        self.completed = True
        self.completed_at = datetime.now()
        self.save()

    def mark_incomplete(self):
        """Marks the task as incomplete."""
        self.completed = False
        self.completed_at = None
        self.save()
