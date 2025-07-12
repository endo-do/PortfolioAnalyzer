"""Initializes the Flask application with session management, blueprints, and startup data loading."""


from flask_login import LoginManager
from flask import Flask
from config import SECRET_KEY
from app.database.connection.pool import init_db_pool
from app.database.tables.exchangerate.fetch_exchangerates import fetch_exchangerates
from app.database.tables.user.get_user_by_id import get_user_by_id
from app.api.Queue import RateLimitedAPIQueue


login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    """
    Initializes and configures the Flask application,
    including ion management, blueprints, and startup routines.

    Returns:
        Flask app instance
    """

    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    app.api_queue = RateLimitedAPIQueue()

    init_db_pool()

    with app.app_context():
        fetch_exchangerates()

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(int(user_id))

    from app.admin import admin_bp
    app.register_blueprint(admin_bp)
    
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes import bp
    app.register_blueprint(bp)

    return app