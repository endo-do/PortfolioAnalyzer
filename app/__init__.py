"""Initializes the Flask application with session management, blueprints, and startup data loading."""


from datetime import date
from flask_login import LoginManager
from flask import Flask, current_app
from config import SECRET_KEY
from app.db import get_user_by_id, get_all_currency_pairs, exchange_rate_exists, get_db_connection, release_db_connection, get_currency_code_by_id, init_db_pool, setup_bondcategories_if_needed
from app.api.twelve_data import get_exchange_rate
from app.api.Queue import RateLimitedAPIQueue


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

    app.api_queue = RateLimitedAPIQueue()

    init_db_pool()

    with app.app_context():
        setup_bondcategories_if_needed()
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
    Fetches or calculates exchangerates for each currency if none are present in the db
    """
        
    currency_pairs = get_all_currency_pairs()
    conn = get_db_connection()
    cursor = conn.cursor()

    new_rates = {}

    for pair in currency_pairs:
        from_id, to_id = pair

        if exchange_rate_exists(from_id, to_id):
            continue

        if from_id == to_id:
            new_rates[(from_id, to_id)] = 1.0

        elif (to_id, from_id) in new_rates:
            rate = new_rates[(to_id, from_id)]
            new_rates[(from_id, to_id)] = 1 / rate

        else:
            rate_data = get_exchange_rate(
                current_app.api_queue,
                f"{get_currency_code_by_id(from_id)}/{get_currency_code_by_id(to_id)}"
            )
            new_rates[(from_id, to_id)] = rate_data["rate"]

    # Insert all collected rates
    for (from_id, to_id), rate in new_rates.items():
        cursor.execute("""
            INSERT INTO exchangerates
                (fromcurrencyid, tocurrencyid, exchangerate, exchangeratelogtime)
                VALUES (%s, %s, %s, %s)
        """, (from_id, to_id, rate, date.today()))

    conn.commit()
    cursor.close()
    release_db_connection(conn)