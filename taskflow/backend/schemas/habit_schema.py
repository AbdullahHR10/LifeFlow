"""Module that contains the Habit schema."""
from marshmallow import Schema, fields, validate
from ..utils.enums import Frequency, Priority, Category, BackgroundColor


class HabitSchema(Schema):
    """Class that defines the schema of Habit."""
    title = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str(required=False)
    frequency = fields.Str(
        required=True,
        validate=validate.OneOf([freq.name for freq in Frequency])
    )
    target_count = fields.Int(required=True)
    current_streak = fields.Int(required=False)
    longest_streak = fields.Int(required=False)
    last_completed = fields.Date(required=False)
    priority = fields.Str(
        required=True,
        validate=validate.OneOf([prio.name for prio in Priority])
    )
    category = fields.Str(
        required=True,
        validate=validate.OneOf([cat.name for cat in Category])
    )
    is_active = fields.Bool(required=False)
    background_color = fields.Str(
        required=False,
        validate=validate.OneOf([color.name for color in BackgroundColor])
    )
