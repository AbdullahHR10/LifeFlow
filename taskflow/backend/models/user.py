"""Module that contains the User class."""
from .base_model import BaseModel
from flask_login import UserMixin
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, validates
from backend.extensions import bcrypt


class User(BaseModel, UserMixin):
    """Represents a user in the application."""
    __tablename__ = "users"
    name = Column(String(30), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    _password = Column("password", String(255), nullable=False)

    tasks = relationship("Task", back_populates="user")
    habits = relationship("Habit", back_populates="user")
    notes = relationship("Note", back_populates="user")
    budgets = relationship("Budget", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

    @property
    def password(self):
        """Raises an error when someone tries to read the raw password."""
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plain_password):
        """Hashes and sets the password."""
        self._password = bcrypt.generate_password_hash(
            plain_password).decode('utf-8')

    def check_password(self, input_password):
        """Checks the user's password."""
        return bcrypt.check_password_hash(self._password, input_password)

    @validates("name")
    def validate_name(self, key: str, value: str) -> str:
        """
        Validates the user's name.

        Parameters:
            key (str): The name of the field being validated ('name').
            value (str): The name to validate.

        Returns:
            str: The validated name value.

        Raises:
            ValueError: If the name is not between 3 and 30 characters.
        """
        if len(value) > 30 or len(value) < 3:
            raise ValueError(f"{key} must be between 3 and 30 characters.")

        return value

    @validates("email")
    def validate_email(self, key: str, value: str) -> str:
        """
        Validates the user's email.

        Parameters:
            key (str): The name of the field being validated ('email').
            value (str): The email address to validate.

        Returns:
            str: The validated email address.

        Raises:
            ValueError: If the email format is invalid.
        """
        value = value.strip().lower()
        if value.count('@') != 1:
            raise ValueError(f"{key} must contain exactly one '@' character.")

        if value.startswith('@') or value.endswith('@'):
            raise ValueError(f"{key} cannot start or end with '@'.")

        if value.startswith('.') or value.endswith('.'):
            raise ValueError(f"{key} cannot start or end with '.'.")

        if '..' in value:
            raise ValueError(f"{key} cannot contain consecutive dots ('..').")

        if '.' not in value.split('@')[1]:
            raise ValueError(f"{key} must contain a dot ('.') after the '@'.")

        return value
