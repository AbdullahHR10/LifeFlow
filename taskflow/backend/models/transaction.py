"""Module that contains the Transaction class."""
from .base_model import BaseModel
from sqlalchemy import (Column, Text, String, Float, Date,
                        ForeignKey, Enum as SqlEnum)
from sqlalchemy.orm import relationship, validates
from ..utils.enums import TransactionType, BudgetCategory
from ..utils.validators import validate_string_field


class Transaction(BaseModel):
    """Represents a transaction in the application."""
    __tablename__ = "transactions"
    title = Column(String(255), nullable=False)
    description = Column(Text)
    amount = Column(Float, nullable=False)
    type = Column(SqlEnum(TransactionType, name="type_enum"), nullable=False)
    date = Column(Date, nullable=False)
    category = Column(SqlEnum(BudgetCategory, name="category_enum"),
                      nullable=False)

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="transactions")

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
            max_length=255
        )
        return value
