"""Module that contains Budget schema tests."""
import pytest
from backend.schemas.budget_schema import BudgetSchema
from marshmallow import ValidationError
from datetime import date

budget_schema = BudgetSchema()


def test_valid_budget_schema():
    """Tests valid budget schema."""
    data = {
        "category": "SALARY",
        "amount": 50.0,
        "spent": 0.0,
        "period": "WEEKLY",
        "start_date": "2025-05-01",
        "end_date": "2026-05-01",
    }
    loaded = budget_schema.load(data)

    assert loaded["category"] == "SALARY"
    assert loaded["amount"] == 50.0
    assert loaded["spent"] == 0.0
    assert loaded["period"] == "WEEKLY"
    assert loaded["start_date"] == date(2025, 5, 1)
    assert loaded["end_date"] == date(2026, 5, 1)


def test_invalid_budget_schema():
    """Tests invalid budget schema."""
    data = {}
    with pytest.raises(ValidationError) as e:
        budget_schema.load(data)

    assert "category" in e.value.messages
    assert "amount" in e.value.messages
    assert "period" in e.value.messages
    assert "start_date" in e.value.messages
    assert "end_date" in e.value.messages

    assert "spent" not in e.value.messages
