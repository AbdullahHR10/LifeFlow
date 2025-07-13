"""Module that contains Transaction schema tests."""
import pytest
from backend.schemas.transaction_schema import TransactionSchema
from marshmallow import ValidationError
from datetime import date

transaction_schema = TransactionSchema()


def test_valid_transaction_schema():
    """Tests valid transaction schema."""
    data = {
        "title": "test",
        "description": "test",
        "amount": 50.0,
        "type": "INCOME",
        "date": "2025-06-30",
        "category": "SALARY"
    }
    loaded = transaction_schema.load(data)

    assert loaded["title"] == "test"
    assert loaded["description"] == "test"
    assert loaded["amount"] == 50.0
    assert loaded["type"] == "INCOME"
    assert loaded["date"] == date(2025, 6, 30)
    assert loaded["category"] == "SALARY"


def test_invalid_transaction_schemaa():
    """Tests invalid transaction schema."""
    data = {}
    with pytest.raises(ValidationError) as e:
        transaction_schema.load(data)
    assert "title" in e.value.messages
    assert "amount" in e.value.messages
    assert "type" in e.value.messages
    assert "date" in e.value.messages
    assert "category" in e.value.messages

    assert "description" not in e.value.messages


def test_transaction_schema_title_too_short():
    """Tests transaction schema title too short."""
    data = {
        "title": "aa",
    }
    with pytest.raises(ValidationError) as e:
        transaction_schema.load(data)
    assert "title" in e.value.messages


def test_transaction_schema_title_too_long():
    """Tests transaction title too long."""
    data = {
        "title": "a" * 256,
    }
    with pytest.raises(ValidationError) as e:
        transaction_schema.load(data)
    assert "title" in e.value.messages
