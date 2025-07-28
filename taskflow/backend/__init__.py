"""Module that sets up the Flask application."""

from flask import Flask, Blueprint
from flask_login import LoginManager
from flask_cors import CORS
from sqlalchemy.orm import declarative_base
from backend.extensions import db, migrate, bcrypt, csrf
from backend.config import Config, TestConfig
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from backend.utils.error_handlers import register_error_handlers
from flasgger import Swagger


Base = declarative_base()
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"
)


def create_app(config_name=None):
    """Creates Flask application."""
    app = Flask(__name__)
    if config_name == "testing":
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)
    Swagger(app, template_file="docs/api_overview.yml")
    register_error_handlers(app)

    CORS(app, supports_credentials=True)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(str(id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return {"status": "error", "message": "Unauthorized"}, 401

    from .routes.auth_routes import auth_bp
    from .routes.task_routes import task_bp
    from .routes.habit_routes import habit_bp
    from .routes.budget_routes import budget_bp
    from .routes.transaction_routes import transaction_bp
    from .routes.note_routes import note_bp

    api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

    api_v1.register_blueprint(auth_bp, url_prefix='/auth')
    api_v1.register_blueprint(task_bp, url_prefix='/tasks')
    api_v1.register_blueprint(habit_bp, url_prefix='/habits')
    api_v1.register_blueprint(budget_bp, url_prefix='/budgets')
    api_v1.register_blueprint(transaction_bp, url_prefix='/transactions')
    api_v1.register_blueprint(note_bp, url_prefix='/notes')

    app.register_blueprint(api_v1, strict_slahes=False)

    from backend.models.base_model import BaseModel
    from backend.models.user import User
    from backend.models.task import Task
    from backend.models.habit import Habit
    from backend.models.budget import Budget
    from backend.models.transaction import Transaction
    from backend.models.note import Note

    return app
