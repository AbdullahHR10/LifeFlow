"""Module that contains the Note class."""
from .base_model import BaseModel
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship


class Note(BaseModel):
    """Represents a note in the application."""
    __tablename__ = "notes"
    title = Column(String(30), nullable=False)
    content = Column(Text, nullable=False) 

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="notes")
