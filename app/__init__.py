# Flask application factory for Portfolio Analyzer - initializes app with authentication, database, logging, and scheduled tasks
"""Initializes the Flask application with session management, blueprints, and startup data loading."""


from flask_login import LoginManager, logout_user
from flask import Flask, flash, redirect, url_for, render_template, request
from flask_wtf.csrf import CSRFProtect
from config import SECRET_KEY, SCHEDULER_HOUR, SCHEDULER_MINUTE, BOOTSTRAP_CSS_URL, BOOTSTRAP_JS_URL, FONT_AWESOME_CSS_URL, CHART_JS_URL, CHART_JS_DATALABELS_URL, API_TIMEOUT_SECONDS, UI_TIMEOUT_MS, UI_UPDATE_DELAY_MS, YAHOO_FINANCE_BASE_URL, YAHOO_FINANCE_QUOTE_URL, YAHOO_FINANCE_LOOKUP_URL, PORTFOLIO_NAME_MAX_LENGTH, PORTFOLIO_DESCRIPTION_MAX_LENGTH, BOND_SYMBOL_MAX_LENGTH, BOND_WEBSITE_MAX_LENGTH, BOND_COUNTRY_MAX_LENGTH, BOND_INDUSTRY_MAX_LENGTH, EXCHANGE_NAME_MAX_LENGTH, CURRENCY_NAME_MAX_LENGTH, CURRENCY_CODE_MAX_LENGTH, CURRENCY_SYMBOL_MAX_LENGTH
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
            try:
                from app.database.helpers.fetch_one import fetch_one
                system_generated = fetch_one("SELECT system_generated FROM status WHERE id = 1")
                
                if system_generated and system_generated[0] is not None:
                    fetch_daily_securityrates()
                else:
                    print("⚠️  Skipping scheduled security rates fetch - database not initialized")
            except Exception as e:
                print(f"⚠️  Scheduled security rates fetch failed: {e}")
    
    def fetch_exchangerates_with_context():
        with app.app_context():
            try:
                from app.database.helpers.fetch_one import fetch_one
                system_generated = fetch_one("SELECT system_generated FROM status WHERE id = 1")
                
                if system_generated and system_generated[0] is not None:
                    fetch_daily_exchangerates()
                else:
                    print("⚠️  Skipping scheduled exchange rates fetch - database not initialized")
            except Exception as e:
                print(f"⚠️  Scheduled exchange rates fetch failed: {e}")
    
    # Schedule to run daily at configured time
    scheduler.add_job(fetch_securityrates_with_context, trigger='cron', hour=SCHEDULER_HOUR, minute=SCHEDULER_MINUTE, id='daily_securityrates')
    scheduler.add_job(fetch_exchangerates_with_context, trigger='cron', hour=SCHEDULER_HOUR, minute=SCHEDULER_MINUTE, id='daily_exchangerates')
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
    
    # Make config values available in templates
    app.config['BOOTSTRAP_CSS_URL'] = BOOTSTRAP_CSS_URL
    app.config['BOOTSTRAP_JS_URL'] = BOOTSTRAP_JS_URL
    app.config['FONT_AWESOME_CSS_URL'] = FONT_AWESOME_CSS_URL
    app.config['CHART_JS_URL'] = CHART_JS_URL
    app.config['CHART_JS_DATALABELS_URL'] = CHART_JS_DATALABELS_URL
    app.config['API_TIMEOUT_SECONDS'] = API_TIMEOUT_SECONDS
    app.config['UI_TIMEOUT_MS'] = UI_TIMEOUT_MS
    app.config['UI_UPDATE_DELAY_MS'] = UI_UPDATE_DELAY_MS
    app.config['YAHOO_FINANCE_BASE_URL'] = YAHOO_FINANCE_BASE_URL
    app.config['YAHOO_FINANCE_QUOTE_URL'] = YAHOO_FINANCE_QUOTE_URL
    app.config['YAHOO_FINANCE_LOOKUP_URL'] = YAHOO_FINANCE_LOOKUP_URL
    app.config['PORTFOLIO_NAME_MAX_LENGTH'] = PORTFOLIO_NAME_MAX_LENGTH
    app.config['PORTFOLIO_DESCRIPTION_MAX_LENGTH'] = PORTFOLIO_DESCRIPTION_MAX_LENGTH
    app.config['BOND_SYMBOL_MAX_LENGTH'] = BOND_SYMBOL_MAX_LENGTH
    app.config['BOND_WEBSITE_MAX_LENGTH'] = BOND_WEBSITE_MAX_LENGTH
    app.config['BOND_COUNTRY_MAX_LENGTH'] = BOND_COUNTRY_MAX_LENGTH
    app.config['BOND_INDUSTRY_MAX_LENGTH'] = BOND_INDUSTRY_MAX_LENGTH
    app.config['EXCHANGE_NAME_MAX_LENGTH'] = EXCHANGE_NAME_MAX_LENGTH
    app.config['CURRENCY_NAME_MAX_LENGTH'] = CURRENCY_NAME_MAX_LENGTH
    app.config['CURRENCY_CODE_MAX_LENGTH'] = CURRENCY_CODE_MAX_LENGTH
    app.config['CURRENCY_SYMBOL_MAX_LENGTH'] = CURRENCY_SYMBOL_MAX_LENGTH

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
            # Try to fetch data with retry logic for Docker environments
            import time
            max_retries = 3
            retry_delay = 5
            
            for attempt in range(max_retries):
                try:
                    from app.database.helpers.fetch_one import fetch_one
                    system_generated = fetch_one("SELECT system_generated FROM status WHERE id = 1")
                    
                    if system_generated and system_generated[0] is not None:
                        # System is initialized, safe to fetch data
                        print("🔄 Fetching initial data...")
                        fetch_daily_exchangerates()
                        fetch_daily_securityrates()
                        print("✅ Initial data fetch completed")
                        break
                    else:
                        if attempt < max_retries - 1:
                            print(f"⚠️  Database not fully initialized (attempt {attempt + 1}/{max_retries}) - retrying in {retry_delay}s...")
                            time.sleep(retry_delay)
                        else:
                            print("⚠️  Database not fully initialized - skipping data fetch during startup")
                            print("ℹ️  Data will be fetched by scheduled tasks once database is ready")
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"⚠️  Database connection failed (attempt {attempt + 1}/{max_retries}): {e}")
                        print(f"ℹ️  Retrying in {retry_delay}s...")
                        time.sleep(retry_delay)
                    else:
                        print(f"⚠️  Could not connect to database after {max_retries} attempts - skipping data fetch")
                        print("ℹ️  Data will be fetched by scheduled tasks once database is ready")
                        break

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