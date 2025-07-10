"""Module that contains BaseSchema."""
from marshmallow import Schema, RAISE


class BaseSchema(Schema):
    """Class that raises errors on unknown fields."""
    class Meta:
        unknown = RAISE
