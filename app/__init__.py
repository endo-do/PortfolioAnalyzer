"""Initializes the Flask application with session management, blueprints, and startup data loading."""


from flask_login import LoginManager, logout_user
from flask import Flask, flash, redirect, url_for
from config import SECRET_KEY
from app.database.connection.pool import init_db_pool
from app.database.tables.exchangerate.fetch_daily_exchangerates import fetch_daily_exchangerates
from app.database.tables.bond.fetch_daily_securityrates import fetch_daily_securityrates
from app.database.tables.user.get_user_by_id import get_user_by_id
from apscheduler.schedulers.background import BackgroundScheduler
from app.database.tables.bond.fetch_daily_securityrates import fetch_daily_securityrates
from app.database.tables.exchangerate.fetch_daily_exchangerates import fetch_daily_exchangerates


login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_daily_securityrates, trigger='interval', days=1)
    scheduler.add_job(fetch_daily_exchangerates, trigger='interval', days=1)
    scheduler.start()

    import atexit
    atexit.register(lambda: scheduler.shutdown())

def create_app():
    """
    Initializes and configures the Flask application,
    including ion management, blueprints, and startup routines.

    Returns:
        Flask app instance
    """

    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    init_db_pool()

    with app.app_context():
        fetch_daily_exchangerates()
        fetch_daily_securityrates()

    start_scheduler(app)

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(int(user_id))

    from app.admin import admin_bp
    app.register_blueprint(admin_bp)
    
    from app.api import api_bp
    app.register_blueprint(api_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes import bp
    app.register_blueprint(bp)

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(str(e))
        flash("An unexpected error occurred. Please try again later.", "danger")
        logout_user()
        return redirect(url_for('auth.login'))
    
    return app