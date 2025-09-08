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
from app.utils.logger import log_user_action, log_error

bp = Blueprint('main', __name__)

# home
@bp.route('/')
@login_required
def home():
    # Normal processing
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
    currencies = fetch_all(query="""SELECT currencyid as id, currencycode FROM currency""", dictionary=True)
    categories = fetch_all(query="""SELECT bondcategoryid as id, bondcategoryname FROM bondcategory""", dictionary=True)
    sectors = fetch_all(query="""SELECT sectorid as id, sectorname, sectordisplayname FROM sector""", dictionary=True)
    regions = fetch_all(query="""SELECT regionid as id, region FROM region""", dictionary=True)
    return render_template('portfolioview.html', portfolio=portfolio, bonds=bonds, currencies=currencies, categories=categories, regions=regions, sectors=sectors)

@bp.route('/securities/<int:portfolio_id>')
@login_required
def securites_view(portfolio_id):
    portfolio = get_portfolio(portfolio_id)
    bonds = get_portfolio_bonds(portfolio_id)
    currencies = fetch_all(query="""SELECT currencyid as id, currencycode FROM currency""", dictionary=True)
    categories = fetch_all(query="""SELECT bondcategoryid as id, bondcategoryname FROM bondcategory""", dictionary=True)
    sectors = fetch_all(query="""SELECT sectorid as id, sectorname, sectordisplayname FROM sector""", dictionary=True)
    regions = fetch_all(query="""SELECT regionid as id, region FROM region""", dictionary=True)
    return render_template('securitiesview.html', portfolio=portfolio, bonds=bonds, currencies=currencies, categories=categories, regions=regions, sectors=sectors)


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
    try:
        new_name = request.form.get('portfolioname', '').strip()
        new_description = request.form.get('portfoliodescription', '').strip()
        selected_symbol = request.form.get('currency_symbol', '').strip()
        
        # Input validation
        if not new_name:
            flash("Portfolio name is required.", "danger")
            return redirect(url_for('main.home'))
        
        if len(new_name) > 50:
            flash("Portfolio name must be 50 characters or less.", "danger")
            return redirect(url_for('main.home'))
        
        if len(new_description) > 255:
            flash("Portfolio description must be 255 characters or less.", "danger")
            return redirect(url_for('main.home'))
        
        if not selected_symbol:
            flash("Currency selection is required.", "danger")
            return redirect(url_for('main.home'))
        
        # Check if portfolio name already exists for this user
        existing_portfolio = fetch_one(
            "SELECT portfolioid FROM portfolio WHERE portfolioname = %s AND userid = %s", 
            (new_name, current_user.id)
        )
        if existing_portfolio:
            flash(f"Portfolio '{new_name}' already exists.", "danger")
            return redirect(url_for('main.home'))
        
        # Get currency ID
        currency_id = fetch_one("SELECT currencyid FROM currency WHERE currencycode = %s", (selected_symbol,))
        if not currency_id:
            flash("Invalid currency selected.", "danger")
            return redirect(url_for('main.home'))
        
        # Create portfolio
        update_query = """
            INSERT INTO portfolio
            SET portfolioname = %s, portfoliodescription = %s, portfoliocurrencyid = %s, userid = %s
        """
        update_args = (new_name, new_description, currency_id[0], current_user.id)
        execute_change_query(query=update_query, args=update_args)
        
        # Log portfolio creation
        log_user_action('PORTFOLIO_CREATED', {
            'portfolio_name': new_name,
            'portfolio_id': None  # We could get this from the insert result
        })
        
        flash(f"Portfolio '{new_name}' has been successfully created", "success")
        return redirect(url_for('main.home'))
        
    except Exception as e:
        log_error(e, {'action': 'create_portfolio', 'user_id': current_user.id})
        flash(f"An error occurred while creating the portfolio: {str(e)}", "danger")
        return redirect(url_for('main.home'))


@bp.route('/delete_portfolio/<int:portfolio_id>', methods=['POST'])
@login_required
def delete_portfolio(portfolio_id):
    try:
        # Verify portfolio exists and belongs to current user
        portfolio = fetch_one(
            "SELECT portfolioname FROM portfolio WHERE portfolioid = %s AND userid = %s",
            (portfolio_id, current_user.id), dictionary=True
        )
        
        if not portfolio:
            flash("Portfolio not found or you don't have permission to delete it.", "danger")
            return redirect(url_for('main.home'))
        
        name = portfolio['portfolioname']
        
        # Delete portfolio (CASCADE will handle related records)
        execute_change_query("DELETE FROM portfolio WHERE portfolioid = %s", (portfolio_id,))
        flash(f"Portfolio '{name}' has been successfully deleted", "success")
        return redirect(url_for('main.home'))
        
    except Exception as e:
        flash(f"An error occurred while deleting the portfolio: {str(e)}", "danger")
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
    try:
        new_name = request.form.get('portfolioname', '').strip()
        new_description = request.form.get('portfoliodescription', '').strip()
        selected_symbol = request.form.get('currency_symbol', '').strip()
        
        # Input validation
        if not new_name:
            flash("Portfolio name is required.", "danger")
            return redirect(url_for('main.portfolioview', portfolio_id=portfolio_id))
        
        if len(new_name) > 50:
            flash("Portfolio name must be 50 characters or less.", "danger")
            return redirect(url_for('main.portfolioview', portfolio_id=portfolio_id))
        
        if len(new_description) > 255:
            flash("Portfolio description must be 255 characters or less.", "danger")
            return redirect(url_for('main.portfolioview', portfolio_id=portfolio_id))
        
        if not selected_symbol:
            flash("Currency selection is required.", "danger")
            return redirect(url_for('main.portfolioview', portfolio_id=portfolio_id))
        
        # Verify portfolio exists and belongs to current user
        portfolio = fetch_one(
            "SELECT portfolioid FROM portfolio WHERE portfolioid = %s AND userid = %s",
            (portfolio_id, current_user.id)
        )
        if not portfolio:
            flash("Portfolio not found or you don't have permission to edit it.", "danger")
            return redirect(url_for('main.home'))
        
        # Check if portfolio name already exists for this user (excluding current portfolio)
        existing_portfolio = fetch_one(
            "SELECT portfolioid FROM portfolio WHERE portfolioname = %s AND userid = %s AND portfolioid != %s", 
            (new_name, current_user.id, portfolio_id)
        )
        if existing_portfolio:
            flash(f"Portfolio '{new_name}' already exists.", "danger")
            return redirect(url_for('main.portfolioview', portfolio_id=portfolio_id))
        
        # Get currency ID
        currency_id = fetch_one("SELECT currencyid FROM currency WHERE currencycode = %s", (selected_symbol,))
        if not currency_id:
            flash("Invalid currency selected.", "danger")
            return redirect(url_for('main.portfolioview', portfolio_id=portfolio_id))
        
        # Update portfolio
        update_query = """
            UPDATE portfolio
            SET portfolioname = %s, portfoliodescription = %s, portfoliocurrencyid = %s
            WHERE portfolioid = %s
        """
        update_args = (new_name, new_description, currency_id[0], portfolio_id)
        execute_change_query(query=update_query, args=update_args)
        flash(f"Portfolio details for '{new_name}' have been successfully updated", "success")
        return redirect(url_for('main.portfolioview', portfolio_id=portfolio_id))
        
    except Exception as e:
        flash(f"An error occurred while updating the portfolio: {str(e)}", "danger")
        return redirect(url_for('main.portfolioview', portfolio_id=portfolio_id))

@bp.route('/portfolio/<int:portfolio_id>/update_securities', methods=['POST'])
@login_required
def update_securities(portfolio_id):
    try:
        # Verify portfolio exists and belongs to current user
        portfolio = fetch_one(
            "SELECT portfolioid FROM portfolio WHERE portfolioid = %s AND userid = %s",
            (portfolio_id, current_user.id)
        )
        if not portfolio:
            flash("Portfolio not found or you don't have permission to edit it.", "danger")
            return redirect(url_for('main.home'))

        if 'new_quantity' in request.form:
            bond_id = request.form.get("change_bond_id", "").strip()
            new_quantity = request.form.get("new_quantity", "").strip()
            
            if not bond_id or not new_quantity:
                flash("Bond ID and quantity are required.", "danger")
                return redirect(url_for('main.edit_portfolio', portfolio_id=portfolio_id))
            
            if not bond_id.isdigit() or not new_quantity.replace('.', '').isdigit():
                flash("Invalid bond ID or quantity format.", "danger")
                return redirect(url_for('main.edit_portfolio', portfolio_id=portfolio_id))
            
            quantity_value = float(new_quantity)
            if quantity_value <= 0:
                flash("Quantity must be greater than 0.", "danger")
                return redirect(url_for('main.edit_portfolio', portfolio_id=portfolio_id))
            
            # Check if bond exists in portfolio
            existing_bond = fetch_one(
                "SELECT bondid FROM portfolio_bond WHERE portfolioid = %s AND bondid = %s",
                (portfolio_id, int(bond_id))
            )
            if not existing_bond:
                flash("Bond not found in portfolio.", "danger")
                return redirect(url_for('main.edit_portfolio', portfolio_id=portfolio_id))
            
            update_query = """
                UPDATE portfolio_bond
                SET quantity = %s
                WHERE portfolioid = %s AND bondid = %s
            """
            execute_change_query(update_query, (quantity_value, portfolio_id, int(bond_id)))
            symbol = fetch_one("SELECT bondsymbol FROM bond WHERE bondid = %s", (bond_id,), dictionary=True)
            if symbol:
                flash(f"Quantity for {symbol['bondsymbol']} has been successfully updated", "success")

        if 'delete_bond' in request.form:
            bond_id = request.form.get('delete_bond', "").strip()
            if not bond_id or not bond_id.isdigit():
                flash("Invalid bond ID.", "danger")
                return redirect(url_for('main.edit_portfolio', portfolio_id=portfolio_id))
            
            # Check if bond exists in portfolio
            existing_bond = fetch_one(
                "SELECT bondid FROM portfolio_bond WHERE portfolioid = %s AND bondid = %s",
                (portfolio_id, int(bond_id))
            )
            if not existing_bond:
                flash("Bond not found in portfolio.", "danger")
                return redirect(url_for('main.edit_portfolio', portfolio_id=portfolio_id))
            
            delete_query = """
                DELETE FROM portfolio_bond
                WHERE portfolioid = %s AND bondid = %s
            """
            execute_change_query(query=delete_query, args=(portfolio_id, int(bond_id)))
            symbol = fetch_one("SELECT bondsymbol FROM bond WHERE bondid = %s", (bond_id,), dictionary=True)
            if symbol:
                flash(f"Security {symbol['bondsymbol']} has been successfully removed", "success")

        if 'add_bond' in request.form:
            bond_id = request.form.get('add_bond', "").strip()
            quantity = request.form.get('quantity', "").strip()
            
            if not bond_id or not quantity:
                flash("Bond ID and quantity are required.", "danger")
                return redirect(url_for('main.edit_portfolio', portfolio_id=portfolio_id))
            
            if not bond_id.isdigit() or not quantity.replace('.', '').isdigit():
                flash("Invalid bond ID or quantity format.", "danger")
                return redirect(url_for('main.edit_portfolio', portfolio_id=portfolio_id))
            
            quantity_value = float(quantity)
            if quantity_value <= 0:
                flash("Quantity must be greater than 0.", "danger")
                return redirect(url_for('main.edit_portfolio', portfolio_id=portfolio_id))
            
            # Check if bond exists
            bond_exists = fetch_one("SELECT bondid FROM bond WHERE bondid = %s", (int(bond_id),))
            if not bond_exists:
                flash("Bond not found.", "danger")
                return redirect(url_for('main.edit_portfolio', portfolio_id=portfolio_id))
            
            # Check if bond already exists in portfolio
            existing_bond = fetch_one(
                "SELECT bondid FROM portfolio_bond WHERE portfolioid = %s AND bondid = %s",
                (portfolio_id, int(bond_id))
            )
            if existing_bond:
                flash("Bond already exists in portfolio.", "danger")
                return redirect(url_for('main.edit_portfolio', portfolio_id=portfolio_id))
            
            insert_query = """
                INSERT INTO portfolio_bond (portfolioid, bondid, quantity)
                VALUES (%s, %s, %s)
            """
            execute_change_query(query=insert_query, args=(portfolio_id, int(bond_id), quantity_value))
            symbol = fetch_one("SELECT bondsymbol FROM bond WHERE bondid = %s", (bond_id,), dictionary=True)
            if symbol:
                flash(f"Security {symbol['bondsymbol']} has been successfully added", "success")

        return redirect(url_for('main.edit_portfolio', portfolio_id=portfolio_id))
        
    except Exception as e:
        flash(f"An error occurred while updating securities: {str(e)}", "danger")
        return redirect(url_for('main.edit_portfolio', portfolio_id=portfolio_id))