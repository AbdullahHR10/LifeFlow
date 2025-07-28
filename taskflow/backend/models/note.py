"""Module that contains the Note class."""
from .base_model import BaseModel
from sqlalchemy import Column, String, Text, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship, validates
from ..utils.enums import BackgroundColor
from ..utils.validators import validate_string_field


class Note(BaseModel):
    """Represents a note in the application."""
    __tablename__ = "notes"
    title = Column(String(30), nullable=False)
    content = Column(Text, nullable=False)
    background_color = Column(SqlEnum(BackgroundColor), nullable=False)

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="notes")

    @validates("title")
    def validate_title(self, key: str, value: str) -> str:
        """
        Validates the note's title.

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
