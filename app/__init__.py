"""Handles Flask app setup, user session managment and blueprint registration"""


from flask_login import LoginManager
from flask import Flask
from config import SECRET_KEY
from app.db import get_user_by_id


login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(int(user_id))


    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes import bp
    app.register_blueprint(bp)

    return app