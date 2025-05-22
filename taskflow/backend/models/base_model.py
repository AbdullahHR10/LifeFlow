"""Module that contains BaseModel."""
from backend import Base, db
from sqlalchemy import Column, String, DateTime
from sqlalchemy.inspection import inspect
from uuid import uuid4
from datetime import datetime, date
from enum import Enum
from backend.utils import ensure_datetime_fields


class BaseModel(Base, db.Model):
    """Defines all common attributes and methods for all the other classes."""
    __abstract__ = True

    id = Column(String(36), nullable=False, primary_key=True,
                default=lambda: str(uuid4()))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, **kwargs):
        """
        Creates an instance of a class.

        Args:
            **kwargs (dict): Keyword arguments
        """
        self.id = str(uuid4())
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if isinstance(value, datetime):
                        value = value.isoformat()
                    elif isinstance(value, Enum):
                        value = value.value
                    setattr(self, key, value)

    def save(self):
        """Saves the object to the database."""
        self.updated_at = datetime.now()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes the object from the database."""
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """Returns a dict with object attributes."""
        dict_rep = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_") and key != "password":
                if isinstance(value, datetime):
                    value = value.isoformat()
                elif isinstance(value, date):
                    value = value.strftime('%Y-%m-%d')
                elif isinstance(value, Enum):
                    value = value.value
                dict_rep[key] = value
        return dict_rep

    def __str__(self):
        """Returns a string representation of the object."""
        dict_rep = self.to_dict()
        return f"[{self.__class__.__name__}] ({self.id}) {dict_rep}"

    def clone(self, **overrides):
        """
        Creates a copy of the model instance with optional field overrides.
        Enforces overriding of fields with unique constraints
        to avoid database conflicts.

        Args:
            **overrides: Field-value pairs to override in the cloned instance.

        Returns:
            A new instance of the same class with copied
            (and overridden) field values.

        Raises:
            ValueError: If any field with a unique constraint or 'password'
            is not overridden.
        """
        cls = self.__class__
        mapper = inspect(cls)
        data = {}
        unique_fields = []

        for column in mapper.columns:
            if column.name in ("id", "created_at", "updated_at", "password"):
                continue
            if column.unique:
                unique_fields.append(column.name)
            data[column.name] = getattr(self, column.name)

        mandatory_fields = unique_fields
        if cls.__name__ == "User":
            mandatory_fields.append("password")

        missing_overrides = [field for field in mandatory_fields
                             if field not in overrides]

        if missing_overrides:
            raise ValueError(f"Must override unique field(s): "
                             f"{', '.join(missing_overrides)}")

        password_plain = None
        if cls.__name__ == "User":
            if "password" not in overrides:
                raise ValueError("Must override 'password' field for User")
            password_plain = overrides.pop("password")

        data.update(overrides)

        for field in unique_fields:
            if field == "password":
                continue
            if cls.query.filter(getattr(cls, field) == data[field]).first():
                raise ValueError(f"'{field}' value '{data[field]}' already exists. Must provide a unique value.")

        instance = cls(**data)
        if cls.__name__ == "User":
            instance.password = password_plain

        ensure_datetime_fields(instance)
        instance.save()
        return instance
