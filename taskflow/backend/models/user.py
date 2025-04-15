"""Moudle that contains the User class."""
from .base_model import BaseModel
from flask_login import UserMixin
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from backend.extensions import bcrypt


class User(BaseModel, UserMixin):
    """Represents a user in the application."""
    __tablename__ = "users"
    name = Column(String(30), nullable=False)
    email = Column(String(255), nullable=False)
    _password = Column("password", String(255), nullable=False)

    tasks = relationship("Task", back_populates="user")
    habits = relationship("Habit", back_populates="user")
    notes = relationship("Note", back_populates="user")

    @property
    def password(self):
        """Raises an error when someone tries to read the raw password."""
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plain_password):
        """Hashes and sets the password."""
        self._password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def check_password(self, input_password):
        """Checks the user's password."""
        return bcrypt.check_password_hash(self._password, input_password)
