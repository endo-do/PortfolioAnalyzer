"""Handles the main routes of the application"""


from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for
from app.database.tables.portfolio.get_portfolio_bonds import get_portfolio_bonds
from app.database.tables.portfolio.get_all_bonds_based_on_portfolio import get_all_bonds_based_on_portfolio
from app.database.tables.portfolio.get_portfolio import get_portfolio
from app.database.tables.portfolio.get_user_portfolios import get_user_portfolios
from app.database.helpers.fetch_all import fetch_all
from app.database.helpers.fetch_one import fetch_one
from app.database.helpers.execute_change_query import execute_change_query
from app.database.helpers.call_procedure import call_procedure


bp = Blueprint('main', __name__)

# home
@bp.route('/')
@login_required
def home():
    portfolios = get_user_portfolios(current_user.id)
    return render_template('home.html', user=current_user, portfolios=portfolios)

@bp.route('/portfolioview/<int:portfolio_id>')
@login_required
def portfolioview(portfolio_id):
    portfolio = get_portfolio(portfolio_id)
    bonds = get_portfolio_bonds(portfolio_id)
    query = """SELECT currencyid as id, currencycode FROM currency"""
    currencies = fetch_all(query=query, dictionary=True)
    return render_template('portfolioview.html', portfolio=portfolio, bonds=bonds, currencies=currencies)

@bp.route('/securityview/<int:bond_id>')
@login_required
def securityview(bond_id):
    return render_template('securityview.html', bond_id=bond_id)

@bp.route('/delete_portfolio/<int:portfolio_id>', methods=['POST'])
@login_required
def delete_portfolio(portfolio_id):
    call_procedure('delete_portfolio', (portfolio_id,))
    return redirect(url_for('main.home'))

@bp.route('/edit_portfolio/<int:portfolio_id>')
@login_required
def edit_portfolio(portfolio_id):
    portfolio = get_portfolio(portfolio_id)
    bonds = get_all_bonds_based_on_portfolio(portfolio_id)
    query = """SELECT currencyid as id, currencycode FROM currency"""
    currencies = fetch_all(query=query, dictionary=True)
    return render_template('edit_portfolio.html', portfolio=portfolio, bonds=bonds, currencies=currencies)

@bp.route('/portfolio/<int:portfolio_id>/update_details', methods=['POST'])
@login_required
def update_portfolio_details(portfolio_id):
    new_name = request.form['portfolioname']
    new_description = request.form['portfoliodescription']
    selected_symbol = request.form['currency_symbol']
    query = "SELECT currencyid FROM currency WHERE currencycode = %s"
    args = (selected_symbol,)
    currency_id = fetch_one(query=query, args=args)
    update_query = """
        UPDATE portfolio
        SET portfolioname = %s, portfoliodescription = %s, portfoliocurrencyid = %s
        WHERE portfolioid = %s
    """
    update_args = (new_name, new_description, currency_id[0], portfolio_id)
    execute_change_query(query=update_query, args=update_args)

    return redirect(url_for('main.portfolioview', portfolio_id=portfolio_id))

@bp.route('/portfolio/<int:portfolio_id>/update_securities', methods=['POST'])
@login_required
def update_securities(portfolio_id):

    if 'save_changes' in request.form:
        for key in request.form:
            if key.startswith('quantities['):
                bond_id = key[len('quantities['):-1]
                quantity = request.form.get(key)
                if bond_id.isdigit() and quantity.isdigit():
                    update_query = """
                        UPDATE portfolio_bond
                        SET quantity = %s
                        WHERE portfolioid = %s AND bondid = %s
                    """
                    update_args = (int(quantity), portfolio_id, int(bond_id))
                    execute_change_query(query=update_query, args=update_args)

    if 'delete_bond' in request.form:
        bond_id = request.form.get('delete_bond')
        if bond_id and bond_id.isdigit():
            delete_query = """
                DELETE FROM portfolio_bond
                WHERE portfolioid = %s AND bondid = %s
            """
            delete_args = (portfolio_id, int(bond_id))
            execute_change_query(query=delete_query, args=delete_args)

    if 'add_bond' in request.form:
        bond_id = request.form.get('add_bond')
        quantity = request.form.get('quantity')
        if bond_id and bond_id.isdigit():
            insert_query = """
                INSERT INTO portfolio_bond (portfolioid, bondid, quantity)
                VALUES (%s, %s, %s)
            """
            insert_args = (portfolio_id, int(bond_id), quantity)
            execute_change_query(query=insert_query, args=insert_args)

    return redirect(url_for('main.edit_portfolio', portfolio_id=portfolio_id))