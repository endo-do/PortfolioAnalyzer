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
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    from app.utils.currency_utils import get_user_default_currency
    base_currency = request.args.get('base_currency', get_user_default_currency(current_user))
    portfolios = get_user_portfolios(current_user.id)
    
    # Convert all portfolio values to base currency for consistent sorting
    from app.database.tables.currency.get_currency_id_by_code import get_currency_id_by_code
    from app.database.helpers.fetch_one import fetch_one
    
    base_currency_id = get_currency_id_by_code(base_currency)
    
    for portfolio in portfolios:
        portfolio_currency_id = get_currency_id_by_code(portfolio['currencycode'])
        if portfolio_currency_id != base_currency_id:
            # Get exchange rate from portfolio currency to base currency
            exchange_rate_query = """
            SELECT exchangerate FROM exchangerate 
            WHERE fromcurrencyid = %s AND tocurrencyid = %s 
            AND exchangeratelogtime = (
                SELECT MAX(exchangeratelogtime) 
                FROM exchangerate 
                WHERE fromcurrencyid = %s AND tocurrencyid = %s
            )
            """
            result = fetch_one(exchange_rate_query, (portfolio_currency_id, base_currency_id, portfolio_currency_id, base_currency_id))
            exchange_rate = float(result[0]) if result else 1.0
            portfolio['converted_value'] = portfolio['total_value'] * exchange_rate
            portfolio['exchange_rate_to_base'] = exchange_rate
        else:
            portfolio['converted_value'] = portfolio['total_value']
            portfolio['exchange_rate_to_base'] = 1.0
    
    query = """SELECT currencyid as id, currencycode FROM currency"""
    currencies = fetch_all(query=query, dictionary=True)
    
    # Calculate total value using converted values
    total_value = sum(portfolio['converted_value'] for portfolio in portfolios) if portfolios else 0
    for p in portfolios:
        p['percentage'] = (p['converted_value'] / total_value * 100) if total_value > 0 else 0
    
    return render_template('home.html', user=current_user, portfolios=portfolios, currencies=currencies, base_currency=base_currency, total_value=total_value)

@bp.route('/portfolioview/<int:portfolio_id>')
@login_required
def portfolioview(portfolio_id):
    from app.utils.currency_utils import get_user_default_currency
    base_currency = request.args.get('base_currency', get_user_default_currency(current_user))
    portfolio = get_portfolio(portfolio_id, base_currency)
    
    # Add exchange rate to portfolio data
    from app.database.tables.currency.get_currency_id_by_code import get_currency_id_by_code
    from app.database.helpers.fetch_one import fetch_one
    
    portfolio_currency_id = get_currency_id_by_code(portfolio['currencycode'])
    base_currency_id = get_currency_id_by_code(base_currency)
    
    if portfolio_currency_id != base_currency_id:
        # Get exchange rate from portfolio currency to base currency
        exchange_rate_query = """
        SELECT exchangerate FROM exchangerate 
        WHERE fromcurrencyid = %s AND tocurrencyid = %s 
        AND exchangeratelogtime = (
            SELECT MAX(exchangeratelogtime) 
            FROM exchangerate 
            WHERE fromcurrencyid = %s AND tocurrencyid = %s
        )
        """
        result = fetch_one(exchange_rate_query, (portfolio_currency_id, base_currency_id, portfolio_currency_id, base_currency_id))
        portfolio['exchange_rate_to_base'] = float(result[0]) if result else 1.0
    else:
        portfolio['exchange_rate_to_base'] = 1.0
    
    bonds = get_portfolio_bonds(portfolio_id, base_currency)
    currencies = fetch_all(query="""SELECT currencyid as id, currencycode FROM currency""", dictionary=True)
    categories = fetch_all(query="""SELECT bondcategoryid as id, bondcategoryname FROM bondcategory""", dictionary=True)
    sectors = fetch_all(query="""SELECT sectorid as id, sectorname, sectordisplayname FROM sector""", dictionary=True)
    regions = fetch_all(query="""SELECT regionid as id, region FROM region""", dictionary=True)
    return render_template('portfolioview.html', portfolio=portfolio, bonds=bonds, currencies=currencies, categories=categories, regions=regions, sectors=sectors, base_currency=base_currency)

@bp.route('/securities/<int:portfolio_id>')
@login_required
def securites_view(portfolio_id):
    from app.utils.currency_utils import get_user_default_currency
    base_currency = request.args.get('base_currency', get_user_default_currency(current_user))
    portfolio = get_portfolio(portfolio_id)
    
    # Add exchange rate to portfolio data
    from app.database.tables.currency.get_currency_id_by_code import get_currency_id_by_code
    from app.database.helpers.fetch_one import fetch_one
    
    portfolio_currency_id = get_currency_id_by_code(portfolio['currencycode'])
    base_currency_id = get_currency_id_by_code(base_currency)
    
    if portfolio_currency_id != base_currency_id:
        # Get exchange rate from portfolio currency to base currency
        exchange_rate_query = """
        SELECT exchangerate FROM exchangerate 
        WHERE fromcurrencyid = %s AND tocurrencyid = %s 
        AND exchangeratelogtime = (
            SELECT MAX(exchangeratelogtime) 
            FROM exchangerate 
            WHERE fromcurrencyid = %s AND tocurrencyid = %s
        )
        """
        result = fetch_one(exchange_rate_query, (portfolio_currency_id, base_currency_id, portfolio_currency_id, base_currency_id))
        portfolio['exchange_rate_to_base'] = float(result[0]) if result else 1.0
    else:
        portfolio['exchange_rate_to_base'] = 1.0
    
    bonds = get_portfolio_bonds(portfolio_id, base_currency)
    currencies = fetch_all(query="""SELECT currencyid as id, currencycode FROM currency""", dictionary=True)
    categories = fetch_all(query="""SELECT bondcategoryid as id, bondcategoryname FROM bondcategory""", dictionary=True)
    sectors = fetch_all(query="""SELECT sectorid as id, sectorname, sectordisplayname FROM sector""", dictionary=True)
    regions = fetch_all(query="""SELECT regionid as id, region FROM region""", dictionary=True)
    return render_template('securitiesview.html', portfolio=portfolio, bonds=bonds, currencies=currencies, categories=categories, regions=regions, sectors=sectors, base_currency=base_currency)


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
    from app.utils.currency_utils import get_user_default_currency
    portfolio = get_portfolio(portfolio_id)
    bonds = get_all_bonds_based_on_portfolio(portfolio_id)
    query = """SELECT currencyid as id, currencycode FROM currency"""
    currencies = fetch_all(query=query, dictionary=True)
    query = """SELECT bondcategoryid as id, bondcategoryname FROM bondcategory"""
    categories = fetch_all(query=query, dictionary=True)
    sectors = fetch_all(query="""SELECT sectorid as id, sectorname, sectordisplayname FROM sector""", dictionary=True)
    regions = fetch_all(query="""SELECT regionid as id, region FROM region""", dictionary=True)
    base_currency = get_user_default_currency(current_user)
    is_admin = current_user.is_admin
    return render_template('edit_portfolio.html', portfolio=portfolio, bonds=bonds, currencies=currencies, categories=categories, regions=regions, sectors=sectors, base_currency=base_currency, is_admin=is_admin)

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

@bp.route('/settings')
@login_required
def settings():
    """User settings page"""
    query = """SELECT currencyid as id, currencycode FROM currency"""
    currencies = fetch_all(query=query, dictionary=True)
    
    # Get user's current currency code
    from app.database.tables.currency.get_currency_code_by_id import get_currency_code_by_id
    current_currency_code = get_currency_code_by_id(current_user.default_base_currency)
    
    # Refresh user data to ensure created_at is loaded
    from app.database.tables.user.get_user_by_id import get_user_by_id
    from flask_login import login_user
    refreshed_user = get_user_by_id(current_user.id)
    if refreshed_user:
        login_user(refreshed_user)
        user_for_template = refreshed_user
    else:
        user_for_template = current_user
    
    return render_template('settings.html', user=user_for_template, currencies=currencies, current_currency_code=current_currency_code)

@bp.route('/settings/update_username', methods=['POST'])
@login_required
def update_username():
    """Update user's username"""
    try:
        new_username = request.form.get('new_username', '').strip()
        
        # Validate input
        if not new_username:
            flash('Username is required.', 'danger')
            return redirect(url_for('main.settings'))
        
        if len(new_username) < 3:
            flash('Username must be at least 3 characters long.', 'danger')
            return redirect(url_for('main.settings'))
        
        if len(new_username) > 50:
            flash('Username must be no more than 50 characters long.', 'danger')
            return redirect(url_for('main.settings'))
        
        # Check if username is the same as current
        if new_username == current_user.username:
            flash('New username is the same as current username.', 'info')
            return redirect(url_for('main.settings'))
        
        # Check if username already exists
        existing_user = fetch_one('SELECT * FROM user WHERE username = %s', (new_username,))
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'danger')
            return redirect(url_for('main.settings'))
        
        # Update username in database
        execute_change_query(
            'UPDATE user SET username = %s WHERE userid = %s',
            (new_username, current_user.id)
        )
        
        # Log the username change
        from app.utils.logger import log_user_action
        log_user_action('USERNAME_CHANGED', {
            'old_username': current_user.username,
            'new_username': new_username
        })
        
        # Reload user data from database and refresh Flask-Login session
        from app.database.tables.user.get_user_by_id import get_user_by_id
        from flask_login import login_user
        updated_user = get_user_by_id(current_user.id)
        if updated_user:
            login_user(updated_user)
        
        flash(f'Username successfully changed to "{new_username}".', 'success')
        return redirect(url_for('main.settings'))
        
    except Exception as e:
        from app.utils.logger import log_error
        log_error(e, {
            'user_id': current_user.id,
            'action': 'update_username'
        })
        flash('An error occurred while updating username. Please try again.', 'danger')
        return redirect(url_for('main.settings'))

@bp.route('/settings/update_email', methods=['POST'])
@login_required
def update_email():
    """Update user's email address"""
    try:
        new_email = request.form.get('new_email', '').strip()
        
        # Validate input
        if not new_email:
            flash('Email address is required.', 'danger')
            return redirect(url_for('main.settings'))
        
        # Basic email validation using regex
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, new_email):
            flash('Please enter a valid email address.', 'danger')
            return redirect(url_for('main.settings'))
        
        # Check if email is the same as current
        if new_email == current_user.email:
            flash('New email is the same as current email.', 'info')
            return redirect(url_for('main.settings'))
        
        # Update email in database
        execute_change_query(
            'UPDATE user SET email = %s WHERE userid = %s',
            (new_email, current_user.id)
        )
        
        # Log the email change
        from app.utils.logger import log_user_action
        log_user_action('EMAIL_CHANGED', {
            'old_email': current_user.email,
            'new_email': new_email
        })
        
        # Reload user data from database and refresh Flask-Login session
        from app.database.tables.user.get_user_by_id import get_user_by_id
        from flask_login import login_user
        updated_user = get_user_by_id(current_user.id)
        if updated_user:
            login_user(updated_user)
        
        flash(f'Email address successfully changed to "{new_email}".', 'success')
        return redirect(url_for('main.settings'))
        
    except Exception as e:
        from app.utils.logger import log_error
        log_error(e, {
            'user_id': current_user.id,
            'action': 'update_email'
        })
        flash('An error occurred while updating email address. Please try again.', 'danger')
        return redirect(url_for('main.settings'))

@bp.route('/settings/update_password', methods=['POST'])
@login_required
def update_password():
    """Update user's password"""
    try:
        current_password = request.form.get('current_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # Validate input
        if not current_password:
            flash('Current password is required.', 'danger')
            return redirect(url_for('main.settings'))
        
        if not new_password:
            flash('New password is required.', 'danger')
            return redirect(url_for('main.settings'))
        
        if not confirm_password:
            flash('Please confirm your new password.', 'danger')
            return redirect(url_for('main.settings'))
        
        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('main.settings'))
        
        # Verify current password
        from werkzeug.security import check_password_hash
        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('main.settings'))
        
        # Check if new password is the same as current
        if check_password_hash(current_user.password, new_password):
            flash('New password is the same as current password.', 'info')
            return redirect(url_for('main.settings'))
        
        # Hash new password and update database
        from werkzeug.security import generate_password_hash
        new_password_hash = generate_password_hash(new_password)
        
        execute_change_query(
            'UPDATE user SET userpwd = %s WHERE userid = %s',
            (new_password_hash, current_user.id)
        )
        
        # Log the password change
        from app.utils.logger import log_user_action
        log_user_action('PASSWORD_CHANGED', {
            'user_id': current_user.id
        })
        
        # Update current_user object
        current_user.password = new_password_hash
        
        flash('Password successfully changed.', 'success')
        return redirect(url_for('main.settings'))
        
    except Exception as e:
        from app.utils.logger import log_error
        log_error(e, {
            'user_id': current_user.id,
            'action': 'update_password'
        })
        flash('An error occurred while updating password. Please try again.', 'danger')
        return redirect(url_for('main.settings'))

@bp.route('/settings/update_currency', methods=['POST'])
@login_required
def update_currency():
    """Update user's default base currency"""
    try:
        new_currency_code = request.form.get('default_currency', '').strip()
        
        # Validate input
        if not new_currency_code:
            flash('Currency selection is required.', 'danger')
            return redirect(url_for('main.settings'))
        
        # Get currency ID from currency code
        from app.database.tables.currency.get_currency_id_by_code import get_currency_id_by_code
        new_currency_id = get_currency_id_by_code(new_currency_code)
        if not new_currency_id:
            flash('Selected currency does not exist.', 'danger')
            return redirect(url_for('main.settings'))
        
        # Check if currency is the same as current
        if new_currency_id == current_user.default_base_currency:
            flash('Selected currency is the same as current currency.', 'info')
            return redirect(url_for('main.settings'))
        
        # Update currency in database
        execute_change_query(
            'UPDATE user SET default_base_currency = %s WHERE userid = %s',
            (new_currency_id, current_user.id)
        )
        
        # Log the currency change
        from app.utils.logger import log_user_action
        log_user_action('DEFAULT_CURRENCY_CHANGED', {
            'old_currency_id': current_user.default_base_currency,
            'new_currency_id': new_currency_id
        })
        
        # Reload user data from database and refresh Flask-Login session
        from app.database.tables.user.get_user_by_id import get_user_by_id
        from flask_login import login_user
        updated_user = get_user_by_id(current_user.id)
        if updated_user:
            login_user(updated_user)
        
        flash('Default base currency successfully updated.', 'success')
        return redirect(url_for('main.settings'))
        
    except Exception as e:
        from app.utils.logger import log_error
        log_error(e, {
            'user_id': current_user.id,
            'action': 'update_currency'
        })
        flash('An error occurred while updating currency. Please try again.', 'danger')
        return redirect(url_for('main.settings'))

@bp.route('/settings/delete_account', methods=['POST'])
@login_required
def delete_account():
    """Delete user's account"""
    try:
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # Validate input
        if not confirm_password:
            flash('Password confirmation is required.', 'danger')
            return redirect(url_for('main.settings'))
        
        # Verify password
        from werkzeug.security import check_password_hash
        if not check_password_hash(current_user.password, confirm_password):
            flash('Password is incorrect.', 'danger')
            return redirect(url_for('main.settings'))
        
        # Prevent original admin account deletion (id=1)
        if current_user.id == 1:
            flash('The original admin account cannot be deleted.', 'danger')
            return redirect(url_for('main.settings'))
        
        # Log the account deletion attempt
        from app.utils.logger import log_user_action
        log_user_action('ACCOUNT_DELETION_ATTEMPT', {
            'user_id': current_user.id,
            'username': current_user.username
        })
        
        # Delete user account (CASCADE will handle related data)
        execute_change_query(
            'DELETE FROM user WHERE userid = %s',
            (current_user.id,)
        )
        
        # Logout user
        from flask_login import logout_user
        logout_user()
        
        flash('Your account has been successfully deleted.', 'success')
        return redirect(url_for('auth.login'))
        
    except Exception as e:
        from app.utils.logger import log_error
        log_error(e, {
            'user_id': current_user.id,
            'action': 'delete_account'
        })
        flash('An error occurred while deleting account. Please try again.', 'danger')
        return redirect(url_for('main.settings'))