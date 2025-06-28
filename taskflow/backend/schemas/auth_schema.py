"""Module that contains the Auth schemas."""
from marshmallow import Schema, fields, validate


class SignupSchema(Schema):
    """Class that defines the schema of Signup."""
    name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=30)
    )
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6)
    )
    confirm_password = fields.Str(required=True)

    def validate(self, data, **kwargs):
        """Validation to ensure the passwords match."""
        errors = super().validate(data)
        if data.get("password") != data.get("confirm_password"):
            errors.setdefault(
                "confirm_password",
                []).append("Passwords do not match.")
            return errors


class LoginSchema(Schema):
    """Class that defines the schema of Login."""
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    remember = fields.Boolean(load_default=False)
