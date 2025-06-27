"""Module that contains error handlers."""

from werkzeug.exceptions import HTTPException
from flask_limiter.errors import RateLimitExceeded
from flask import request
from flask_login import current_user
from .response import json_response
from .logger import logger


def register_error_handlers(app):
    """Error handlers registration."""
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Handles HTTPException."""
        return json_response(
            status="error",
            message=e.description
        ), e.code

    @app.errorhandler(Exception)
    def handle_general_exception(e):
        """Handles Exception."""
        logger.exception(f"Unhandled Exception: {str(e)}")
        return json_response(
            status="error",
            message="Internal server error"
        ), 500

    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit(e):
        """Handles rate limit."""
        user_id = current_user.id if current_user.is_authenticated \
            else "Anonymous"
        ip_address = request.remote_addr or "Unknown IP"

        logger.warning(f"Rate limit exceeded by User {user_id}: "
                       f"IP {ip_address}, path: {request.path}")
        return json_response(
            status="error",
            message="Too many requests. Please try again later."
        ), 429
