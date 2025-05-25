"""Initializes the Flask application with session management, blueprints, and startup data loading."""


from datetime import date
from flask_login import LoginManager
from flask import Flask
from config import SECRET_KEY
from app.db import get_user_by_id, get_all_currency_pairs, exchange_rate_exists, get_db_connection, release_db_connection, get_currency_code_by_id, init_db_pool
from app.api.twelve_data import get_exchange_rate


login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    """
    Initializes and configures the Flask application,
    including session management, blueprints, and startup routines.

    Returns:
        Flask app instance
    """

    app = Flask(__name__)
    app.secret_key = SECRET_KEY


    init_db_pool()

    with app.app_context():
        fetch_startup_data()

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(int(user_id))

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes import bp
    app.register_blueprint(bp)

    return app

def fetch_startup_data():
    """
    Fetches today exchangerates if needed
    """
    
    currency_pairs = get_all_currency_pairs()
    conn = get_db_connection()
    cursor = conn.cursor()

    for pair in currency_pairs:
        
        if not exchange_rate_exists(pair[0], pair[1], date.today()):
        
            if pair[0] == pair[1]:
                cursor.execute("""
                    INSERT INTO exchangerates
                        (fromcurrencyid, tocurrencyid, exchangerate, exchangeratelogtime)
                        VALUES (%s, %s, %s, %s)""",
                        (pair[0], pair[1], 1.0, date.today()))
                continue
            
            rate_data = get_exchange_rate(f"{get_currency_code_by_id(pair[0])}/{get_currency_code_by_id(pair[1])}")
            
            if rate_data and "rate" in rate_data:
                cursor.execute("""
                    INSERT INTO exchangerates
                        (fromcurrencyid, tocurrencyid, exchangerate, exchangeratelogtime)
                        VALUES (%s, %s, %s, %s)""",
                        (pair[0], pair[1], rate_data["rate"], date.today()))
    conn.commit()
    cursor.close()
    release_db_connection(conn)