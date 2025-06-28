"""Module that contains the ownership_required decorator."""
from functools import wraps
from flask import abort
from flask_login import current_user
from ..utils.db_helpers import get_object


def ownership_required(model):
    """Decorator that ensures the current user owns the object."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            obj_key = f"{model.__name__.lower()}_id"
            obj_id = kwargs.pop(obj_key, None)
            if not obj_id:
                abort(400, description="Missing object ID")

            obj = get_object(model, obj_id)
            if not obj:
                abort(404, description=f"{model.__name__} not found")

            if obj.user_id != current_user.id:
                abort(403, description="You do not have permission to "
                      f"access this resource")

            kwargs[model.__name__.lower()] = obj
            return f(*args, **kwargs)

        return decorated_function
    return decorator
