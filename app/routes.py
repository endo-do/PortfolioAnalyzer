"""Handles the main routes of the application"""


from flask_login import login_required, current_user
from flask import Blueprint, render_template, abort
from app.database.user_data import get_user_portfolios
from app.database.portfolio_data import get_portfolio_by_id, get_portfolio_bonds
from app.database.db import fetch_user_data


bp = Blueprint('main', __name__)

# home
@bp.route('/')
@login_required
def home():
    fetch_user_data(current_user.id)
    portfolios = get_user_portfolios(current_user.id)
    return render_template('home.html', user=current_user, portfolios=portfolios)

@bp.route('/portfolioview/<int:portfolio_id>')
@login_required
def portfolioview(portfolio_id):
    portfolio = get_portfolio_by_id(portfolio_id)
    if not portfolio:
        abort(404)  # Portfolio not found
    user_portfolios = get_user_portfolios(current_user.id)
    bonds = get_portfolio_bonds(portfolio_id)
    portfolio = portfolio | user_portfolios[portfolio_id-1]
    return render_template('portfolioview.html', portfolio=portfolio, bonds=bonds)