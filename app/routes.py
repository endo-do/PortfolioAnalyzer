"""Handles the main routes of the application"""


from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database.tables.portfolio.get_portfolio_bonds import get_portfolio_bonds
from app.database.tables.portfolio.get_all_bonds_based_on_portfolio import get_all_bonds_based_on_portfolio
from app.database.tables.portfolio.get_portfolio import get_portfolio
from app.database.tables.portfolio.get_user_portfolios import get_user_portfolios
from app.database.helpers.fetch_all import fetch_all
from app.database.helpers.fetch_one import fetch_one
from app.database.helpers.execute_change_query import execute_change_query
from app.database.helpers.call_procedure import call_procedure
from app.database.tables.bond.get_full_bond import get_full_bond


bp = Blueprint('main', __name__)

# home
@bp.route('/')
def home():
    if not current_user.is_authenticated:
        # Redirect silently without flash
        return redirect(url_for('auth.login'))
    # else normal processing
    portfolios = get_user_portfolios(current_user.id)
    query = """SELECT currencyid as id, currencycode FROM currency"""
    currencies = fetch_all(query=query, dictionary=True)
    total_value = sum(portfolio['total_value'] for portfolio in portfolios) if portfolios else 0
    for p in portfolios:
        p['percentage'] = (p['total_value'] / total_value * 100) if total_value > 0 else 0
    return render_template('home.html', user=current_user, portfolios=portfolios, currencies=currencies)

@bp.route('/portfolioview/<int:portfolio_id>')
@login_required
def portfolioview(portfolio_id):
    portfolio = get_portfolio(portfolio_id)
    bonds = get_portfolio_bonds(portfolio_id)
    query = """SELECT currencyid as id, currencycode FROM currency"""
    currencies = fetch_all(query=query, dictionary=True)
    query = """SELECT bondcategoryid as id, bondcategoryname FROM bondcategory"""
    categories = fetch_all(query=query, dictionary=True)
    return render_template('portfolioview.html', portfolio=portfolio, bonds=bonds, currencies=currencies, categories=categories)

@bp.route('/securityview/<int:bond_id>/<int:portfolio_id>')
@login_required
def securityview(bond_id, portfolio_id):
    bond = get_full_bond(bond_id)
    query = """SELECT currencyid, currencycode FROM currency"""
    currencies = fetch_all(query=query, dictionary=True)
    query = """SELECT bondcategoryid, bondcategoryname FROM bondcategory"""
    categories = fetch_all(query=query, dictionary=True)
    return render_template('securityview.html', bond=bond, portfolio_id=portfolio_id, currencies=currencies, categories=categories)

@bp.route('/create_portfolio', methods=['POST'])
@login_required
def create_portfolio():
    new_name = request.form['portfolioname']
    new_description = request.form['portfoliodescription']
    selected_symbol = request.form['currency_symbol']
    query = "SELECT currencyid FROM currency WHERE currencycode = %s"
    args = (selected_symbol,)
    currency_id = fetch_one(query=query, args=args)
    update_query = """
        INSERT INTO portfolio
        SET portfolioname = %s, portfoliodescription = %s, portfoliocurrencyid = %s, userid = %s
    """
    update_args = (new_name, new_description, currency_id[0], current_user.id)
    execute_change_query(query=update_query, args=update_args)
    flash(f"Portfolio {new_name} has been succesfully created", "success")
    return redirect(url_for('main.home'))


@bp.route('/delete_portfolio/<int:portfolio_id>', methods=['POST'])
@login_required
def delete_portfolio(portfolio_id):
    name = fetch_one("""SELECT portfolioname FROM portfolio where portfolioid = %s""",
                     (portfolio_id,), dictionary=True)['portfolioname']
    execute_change_query("""
        DELETE FROM portfolio WHERE portfolioid = %s
    """, (portfolio_id,))
    flash(f"Portfolio {name} has been succesfully deleted", "success")
    return redirect(url_for('main.home'))

@bp.route('/edit_portfolio/<int:portfolio_id>')
@login_required
def edit_portfolio(portfolio_id):
    portfolio = get_portfolio(portfolio_id)
    bonds = get_all_bonds_based_on_portfolio(portfolio_id)
    query = """SELECT currencyid as id, currencycode FROM currency"""
    currencies = fetch_all(query=query, dictionary=True)
    query = """SELECT bondcategoryid as id, bondcategoryname FROM bondcategory"""
    categories = fetch_all(query=query, dictionary=True)
    return render_template('edit_portfolio.html', portfolio=portfolio, bonds=bonds, currencies=currencies, categories=categories)

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
    flash(f"Portfolio Details for {new_name} have been successfully updated", "success")
    return redirect(url_for('main.portfolioview', portfolio_id=portfolio_id))

@bp.route('/portfolio/<int:portfolio_id>/update_securities', methods=['POST'])
@login_required
def update_securities(portfolio_id):

    if 'new_quantity' in request.form:
        bond_id = request.form.get("change_bond_id")
        new_quantity = request.form.get("new_quantity")
        if bond_id and new_quantity and bond_id.isdigit() and new_quantity.isdigit():
            update_query = """
                UPDATE portfolio_bond
                SET quantity = %s
                WHERE portfolioid = %s AND bondid = %s
            """
            execute_change_query(update_query, (int(new_quantity), portfolio_id, int(bond_id)))
            symbol = fetch_one("""SELECT bondsymbol FROM bond where bondid = %s""",
                               (bond_id,), dictionary=True)['bondsymbol']
            flash(f"Quantity for {symbol} has been successfully updated", "success")

    if 'delete_bond' in request.form:
        bond_id = request.form.get('delete_bond')
        if bond_id and bond_id.isdigit():
            delete_query = """
                DELETE FROM portfolio_bond
                WHERE portfolioid = %s AND bondid = %s
            """
            delete_args = (portfolio_id, int(bond_id))
            execute_change_query(query=delete_query, args=delete_args)
            symbol = fetch_one("""SELECT bondsymbol FROM bond where bondid = %s""",
                    (bond_id,), dictionary=True)['bondsymbol']
            flash(f"Security {symbol} has been successfully removed", "success")

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
            symbol = fetch_one("""SELECT bondsymbol FROM bond where bondid = %s""",
                    (bond_id,), dictionary=True)['bondsymbol']
            flash(f"Security {symbol} has been successfully added", "success")

    return redirect(url_for('main.edit_portfolio', portfolio_id=portfolio_id))