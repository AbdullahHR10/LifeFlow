"""Module that contains the Transaction class."""
from .base_model import BaseModel
from sqlalchemy import (Column, Text, String, Float, Date,
                        ForeignKey, Enum as SqlEnum)
from sqlalchemy.orm import relationship
from ..utils.enums import TransactionType, BudgetCategory


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
