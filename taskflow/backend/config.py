"""Module that contains the Config class."""
import os
from redis import Redis


class Config():
    """Configuration for the Flask application."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'taskflow:'
    SESSION_REDIS = Redis(
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=int(os.environ.get("REDIS_PORT", 6379))
    )


class TestConfig():
    """Configuration for testing the Flask application."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "testing-secret-key"
    RATELIMIT_STORAGE_URL = "memory://"
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SESSION_KEY_PREFIX = "taskflow_test:"
