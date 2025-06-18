"""Module that contains BaseModel."""
from backend import Base, db
from sqlalchemy import Column, String, DateTime
from uuid import uuid4
from datetime import datetime, date
from enum import Enum
from backend.utils.converters import str_to_datetime


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

    def save(self, refresh=False):
        """Saves the object to the database."""
        self.updated_at = datetime.now()
        str_to_datetime(self)
        db.session.add(self)
        db.session.commit()
        if refresh:
            db.session.refresh(self)

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
