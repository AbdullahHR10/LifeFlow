"""Module that contains the Config class."""
import os
from redis import Redis
import logging

class Config():
    """Configuration for the Flask application."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'taskflow:'
    SESSION_REDIS = Redis(host='localhost', port=6379)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s"
        )

class TestConfig():
    """Configuration for testing the Flask application."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_KEY_PREFIX = "taskflow_test:"
    SESSION_REDIS = Redis(host="localhost", port=6379)
