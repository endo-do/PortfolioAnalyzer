"""Handles the main routes of the application"""


from flask_login import login_required, current_user
from flask import Blueprint, render_template
from .db import get_user_portfolios


bp = Blueprint('main', __name__)

# home
@bp.route("/")
@login_required
def home():
    portfolios = get_user_portfolios(current_user.id)
    return render_template('home.html', user=current_user, portfolios=portfolios)
