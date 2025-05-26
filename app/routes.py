"""Handles the main routes of the application"""


from flask_login import login_required, current_user
from flask import Blueprint, render_template
from app.database.get_data import get_user_portfolios
from app.database.db import fetch_user_data


bp = Blueprint('main', __name__)

# home
@bp.route("/")
@login_required
def home():
    fetch_user_data(current_user.id)
    portfolios = get_user_portfolios(current_user.id)
    return render_template('home.html', user=current_user, portfolios=portfolios)