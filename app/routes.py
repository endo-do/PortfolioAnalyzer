"""Handles the main routes of the application"""


from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for
from app.database.tables.portfolio.get_portfolio_bonds import get_portfolio_bonds
from app.database.tables.portfolio.get_portfolio import get_portfolio
from app.database.tables.portfolio.get_user_portfolios import get_user_portfolios
from app.database.tables.user.fetch_user_data import fetch_user_data
from app.database.helpers.fetch_all import fetch_all
from app.database.helpers.fetch_one import fetch_one


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
    portfolio = get_portfolio(portfolio_id)
    bonds = get_portfolio_bonds(portfolio_id)
    query = """SELECT currencyid as id, currencycode FROM currency"""
    currencies = fetch_all(query=query)
    return render_template('portfolioview.html', portfolio=portfolio, bonds=bonds, currencies=currencies)

@bp.route('/edit_portfolio/<int:portfolio_id>')
@login_required
def edit_portfolio(portfolio_id):
    return render_template('edit_portfolio.html')

@bp.route('/portfolio/<int:portfolio_id>/update', methods=['POST'])
@login_required
def update_portfolio(portfolio_id):
    new_name = request.form['portfolioname']
    new_description = request.form['portfoliodescription']
    selected_symbol = request.form['currency_symbol']

    # Get currency ID from symbol
    query = "SELECT currencyid FROM currency WHERE currencycode = %s"
    args = (selected_symbol,)
    currency_id = fetch_one(query=query, args=args)
    
    #(new_name, new_description, currency_id, portfolio_id)

    return redirect(url_for('main.portfolioview', portfolio_id=portfolio_id))