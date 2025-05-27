"""Moudle that contains the Task class."""
from .base_model import BaseModel
from sqlalchemy import (Column,
                        String, Text, Date, Boolean,
                        Enum as SqlEnum, ForeignKey)
from sqlalchemy.orm import relationship
from enum import Enum


class Priority(Enum):
    """Task priority enum."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class Category(Enum):
    """Task category enum."""
    WORK = "Work"
    PERSONAL = "Personal"
    STUDY = "Study"
    HEALTH = "Health"
    HOBBY = "Hobby"
    OTHER = "Other"


class Task(BaseModel):
    """Represents a task in the application."""
    __tablename__ = "tasks"
    title = Column(String(30), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(SqlEnum(Priority, name="priority_enum"), nullable=False)
    deadline = Column(Date, nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
    category = Column(SqlEnum(Category, name="category_enum"), nullable=False)
    completed_at = Column(Date, nullable=True)

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="tasks")
