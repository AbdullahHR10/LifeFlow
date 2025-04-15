"""Moudle that contains the Task class."""
from .base_model import BaseModel
from sqlalchemy import (Column,
                        String, Text, Date, Enum as SqlEnum, ForeignKey)
from sqlalchemy.orm import relationship
from enum import Enum


class Priority(Enum):
    """Task priority enum."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "HIGH"
    CRITICAL = "Critical"


class Task(BaseModel):
    """Represents a task in the application."""
    __tablename__ = "tasks"
    name = Column(String(30), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(SqlEnum(Priority, name="priority_enum"), nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(String(20), default="pending")

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="tasks")
