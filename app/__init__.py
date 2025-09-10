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

# Configure Flask-Login to return 401 instead of redirects in test mode
def unauthorized_handler():
    from flask import request
    if request.is_json or 'test' in request.headers.get('User-Agent', '').lower():
        from flask import abort
        abort(401)
    return redirect(login_manager.login_view)

login_manager.unauthorized_handler(unauthorized_handler)

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    
    # Schedule daily updates with proper app context to avoid blocking users
    def fetch_securityrates_with_context():
        with app.app_context():
            fetch_daily_securityrates()
    
    def fetch_exchangerates_with_context():
        with app.app_context():
            fetch_daily_exchangerates()
    
    # Schedule to run daily at midnight (00:00) regardless of app start time
    scheduler.add_job(fetch_securityrates_with_context, trigger='cron', hour=0, minute=0, id='daily_securityrates')
    scheduler.add_job(fetch_exchangerates_with_context, trigger='cron', hour=0, minute=0, id='daily_exchangerates')
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

    # Disable CSRF protection in test environment
    import os
    if os.environ.get('FLASK_ENV') == 'testing' or 'pytest' in os.environ.get('_', ''):
        app.config['WTF_CSRF_ENABLED'] = False
    
    # Initialize CSRF protection
    csrf.init_app(app)

    # Initialize logging system
    setup_logging(app)

    init_db_pool()

    # Skip data fetching during testing
    if not app.config.get('TESTING', False):
        with app.app_context():
            fetch_daily_exchangerates()
            fetch_daily_securityrates()

    # Skip scheduler during testing
    if not app.config.get('TESTING', False):
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