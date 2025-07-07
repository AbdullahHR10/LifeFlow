"""Module that contains the Budget class."""
from .base_model import BaseModel
from sqlalchemy import (Column, String, Float, Date,
                        ForeignKey, Enum as SqlEnum)
from sqlalchemy.orm import relationship
from ..utils.enums import (
    BudgetCategory, BudgetPeriod, BudgetCategory, TransactionType
)
from ..models.transaction import Transaction
from datetime import date

class Budget(BaseModel):
    """Represents a budget in the application."""
    __tablename__ = "budgets"
    category = Column(SqlEnum(BudgetCategory, name="category_enum"),
                      nullable=False)
    amount = Column(Float, nullable=False)
    spent = Column(Float, nullable=False, default=0.0)
    period = Column(SqlEnum(BudgetPeriod, name="period_enum"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="budgets")

    def recalculate_budget(self, start_date: date, end_date: date) -> None:
        """Recalculates and updates the spent amount for the user's budget."""
        expenses = Transaction.query.filter_by(
            user_id=self.user_id,
            category=self.category,
            type=TransactionType.EXPENSE
        ).filter(
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).all()

        self.spent = sum(e.amount for e in expenses)
        self.save()
