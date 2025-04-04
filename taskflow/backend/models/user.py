"""Moudle that contains the User class."""
from .base_model import BaseModel
from flask_login import UserMixin
from sqlalchemy import Column, String


class User(BaseModel, UserMixin):
    """Represents a user in the application."""
    __tablename__ = "users"
    name = Column(String(30), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
