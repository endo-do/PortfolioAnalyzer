"""Initializes the Flask application with session management, blueprints, and startup data loading."""


from flask_login import LoginManager, logout_user
from flask import Flask, flash, redirect, url_for, render_template, request
from flask_wtf.csrf import CSRFProtect
from config import SECRET_KEY
from app.database.connection.pool import init_db_pool
from app.database.tables.exchangerate.fetch_daily_exchangerates import fetch_daily_exchangerates
from app.database.tables.bond.fetch_daily_securityrates import fetch_daily_securityrates
from app.database.tables.user.get_user_by_id import get_user_by_id
from apscheduler.schedulers.background import BackgroundScheduler
from app.database.tables.bond.fetch_daily_securityrates import fetch_daily_securityrates
from app.database.tables.exchangerate.fetch_daily_exchangerates import fetch_daily_exchangerates
from werkzeug.exceptions import HTTPException
from app.utils.logger import setup_logging, log_error, log_security_event


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()

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

    # Initialize CSRF protection
    csrf.init_app(app)

    # Initialize logging system
    setup_logging(app)

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
        if isinstance(e, HTTPException) and e.code == 404 and request.path == "/favicon.ico":
            return "", 404
        else:
            # Handle real unexpected errors
            # Import current_user conditionally to avoid import errors
            try:
                from flask_login import current_user
                user_id = current_user.id if hasattr(current_user, 'id') and current_user.is_authenticated else None
            except (ImportError, AttributeError):
                user_id = None
            
            log_error(e, {
                'url': request.url if request else 'N/A',
                'method': request.method if request else 'N/A',
                'user_id': user_id
            })
            flash("An unexpected error occurred. Please try again later.", "danger")
            # Import logout_user conditionally
            try:
                from flask_login import logout_user
                logout_user()
            except (ImportError, AttributeError):
                pass  # If logout_user is not available, just continue
            return redirect(url_for("auth.login"))
    
    return app