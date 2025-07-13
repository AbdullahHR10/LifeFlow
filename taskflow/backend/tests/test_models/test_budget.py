"""Module that contains Budget class tests."""
import pytest
from backend.models import Budget, Transaction
from backend.utils.enums import BudgetCategory, Frequency, TransactionType
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError


def test_budget_valid():
    """Tests valid budget."""
    budget = Budget(
        category=BudgetCategory.SALARY,
        amount=50.0,
        spent=0.0,
        period=Frequency.WEEKLY,
        start_date=date(2025, 5, 1),
        end_date=date(2026, 5, 1)
    )

    assert isinstance(budget.category, BudgetCategory)
    assert budget.category == BudgetCategory.SALARY
    assert isinstance(budget.amount, float)
    assert budget.amount == 50.0
    assert isinstance(budget.spent, float)
    assert budget.spent == 0
    assert isinstance(budget.period, Frequency)
    assert budget.period == Frequency.WEEKLY
    assert isinstance(budget.start_date, date)
    assert budget.start_date == date(2025, 5, 1)
    assert isinstance(budget.end_date, date)
    assert budget.end_date == date(2026, 5, 1)


def tests_budget_to_dict(budget):
    """Tests to_dict handles enum and date values."""
    expected = {
        "category": "SALARY",
        "amount": 50.0,
        "spent": 0.0,
        "period": "WEEKLY",
        "start_date": "2025-05-01",
        "end_date": "2026-05-01",
    }

    d = budget.to_dict()
    for key, value in expected.items():
        assert d[key] == value


def test_budget_missing_amount_raises(app):
    """Tests budget with missing amount."""
    budget = Budget(
        category=BudgetCategory.SALARY,
        spent=0.0,
        period=Frequency.WEEKLY,
        start_date=date(2025, 5, 1),
        end_date=date(2026, 5, 1)
    )
    with pytest.raises(IntegrityError):
        budget.save()


def test_recalculate_budget_updates_spent(app, user):
    """Tests recalculate_budget."""
    budget = Budget(
        category=BudgetCategory.SALARY,
        amount=5000.0,
        spent=0.0,
        period=Frequency.MONTHLY,
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        user_id=user.id
    )
    budget.save()

    t1 = Transaction(
        title="test",
        category=BudgetCategory.SALARY,
        amount=500.0,
        date=date(2025, 3, 10),
        type=TransactionType.EXPENSE,
        user_id=user.id
    )
    t1.save()

    t2 = Transaction(
        title="test",
        description="test",
        category=BudgetCategory.SALARY,
        amount=250.5,
        date=date(2025, 3, 10),
        type=TransactionType.EXPENSE,
        user_id=user.id
    )
    t2.save()

    budget.recalculate_budget()

    assert budget.spent == 750.5
