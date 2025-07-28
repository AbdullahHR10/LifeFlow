"""Module that contains the Note schema."""
from marshmallow import fields, validate
from ..utils.enums import BackgroundColor
from . import BaseSchema


class NoteSchema(BaseSchema):
    """Class that defines the schema of Note."""
    title = fields.Str(required=True, validate=validate.Length(min=3, max=30))
    content = fields.Str(required=True, validate=validate.Length(min=1))
    background_color = fields.Str(
        required=True,
        validate=validate.OneOf([color.name for color in BackgroundColor])
    )
