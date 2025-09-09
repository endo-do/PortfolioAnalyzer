"""Admin routes for managing securities, currencies, and users."""

from datetime import date
from flask import render_template, url_for, redirect, request, flash, session
from flask_login import login_required, current_user
import mysql.connector
from werkzeug.security import generate_password_hash
from app.admin import admin_bp
from app.admin.admin_required import admin_required
from app.api.get_eod import get_eod
from app.database.helpers.fetch_all import fetch_all
from app.database.helpers.fetch_one import fetch_one
from app.database.helpers.execute_change_query import execute_change_query
from app.database.tables.bond.get_all_bonds import get_all_bonds
from app.database.tables.bond.get_full_bond import get_full_bond
from app.database.tables.exchangerate.fetch_daily_exchangerates import fetch_daily_exchangerates
from app.database.tables.currency.get_all_currencies import get_all_currencies
from app.database.tables.bondcategory.get_all_bondcategories import get_all_categories
from app.database.tables.user.get_all_users import get_all_users
from app.api.get_exchange import get_exchange
from app.admin.log_viewer import get_log_files, read_log_file, get_log_statistics
from app.utils.logger import log_user_action, log_security_event, log_error

@admin_bp.route('/')
@admin_required
def admin_dashboard():
    try:
        # Fetch statistics for the dashboard
        stats = {}
        
        # Get total users count
        users_result = fetch_one("SELECT COUNT(*) as count FROM user")
        stats['total_users'] = users_result[0] if users_result else 0
        
        # Get total securities count
        securities_result = fetch_one("SELECT COUNT(*) as count FROM bond")
        stats['total_securities'] = securities_result[0] if securities_result else 0
        
        # Get total portfolios count
        portfolios_result = fetch_one("SELECT COUNT(*) as count FROM portfolio")
        stats['total_portfolios'] = portfolios_result[0] if portfolios_result else 0
        
        # Get total currencies count
        currencies_result = fetch_one("SELECT COUNT(*) as count FROM currency")
        stats['total_currencies'] = currencies_result[0] if currencies_result else 0
        
        # Log admin dashboard access
        log_user_action('ADMIN_DASHBOARD_ACCESS', {
            'total_users': stats['total_users'],
            'total_securities': stats['total_securities'],
            'total_portfolios': stats['total_portfolios'],
            'total_currencies': stats['total_currencies']
        })
        
        return render_template('admin_dashboard.html', stats=stats)
        
    except Exception as e:
        log_error(e, {'action': 'admin_dashboard', 'user_id': current_user.id})
        # Return template with empty stats if there's an error
        return render_template('admin_dashboard.html', stats={})

@admin_bp.route('/logs')
@admin_required
def view_logs():
    try:
        log_files = get_log_files()
        log_stats = get_log_statistics()
        
        # Log admin access to logs
        log_user_action('ADMIN_VIEWED_LOGS', {
            'log_files_count': len(log_files),
            'total_size_mb': log_stats['total_size_mb']
        })
        
        return render_template('log_viewer.html', log_files=log_files, log_stats=log_stats)
    except Exception as e:
        log_error(e, {'action': 'view_logs', 'user_id': current_user.id})
        flash(f"Error accessing logs: {str(e)}", "danger")
        return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/logs/<filename>')
@admin_required
def view_log_file(filename):
    try:
        lines = request.args.get('lines', 100, type=int)
        log_lines = read_log_file(filename, lines)
        
        if log_lines is None:
            flash(f"Log file '{filename}' not found or access denied.", "danger")
            return redirect(url_for('admin.view_logs'))
        
        # Log admin access to specific log file
        log_user_action('ADMIN_VIEWED_LOG_FILE', {
            'filename': filename,
            'lines_requested': lines,
            'lines_returned': len(log_lines)
        })
        
        return render_template('log_file_viewer.html', 
                             filename=filename, 
                             log_lines=log_lines,
                             lines_count=len(log_lines))
    except Exception as e:
        log_error(e, {'action': 'view_log_file', 'filename': filename, 'user_id': current_user.id})
        flash(f"Error reading log file: {str(e)}", "danger")
        return redirect(url_for('admin.view_logs'))

@admin_bp.route('/securityoverview')
@admin_required
def securityoverview():
    base_currency = 'USD'  # Fixed to USD for now, user can set this later in options
    bonds = get_all_bonds()
    for bond in bonds:
        if bond['bondrate'] == 'N/A':
            bond['bondrate'] = None
        else:
            try:
                bond['bondrate'] = float(bond['bondrate'])
            except ValueError:
                bond['bondrate'] = None
    
    # Add exchange rate data for currency conversion
    from app.database.tables.currency.get_currency_id_by_code import get_currency_id_by_code
    from app.database.helpers.fetch_one import fetch_one
    
    base_currency_id = get_currency_id_by_code(base_currency)
    
    for bond in bonds:
        if bond['bondrate'] is not None:
            bond_currency_id = get_currency_id_by_code(bond['currencycode'])
            if bond_currency_id == base_currency_id:
                bond['exchange_rate_to_base'] = 1.0
            else:
                # Get exchange rate from database
                exchange_rate_query = """
                SELECT exchangerate FROM exchangerate 
                WHERE fromcurrencyid = %s AND tocurrencyid = %s 
                AND exchangeratelogtime = (
                    SELECT MAX(exchangeratelogtime) 
                    FROM exchangerate 
                    WHERE fromcurrencyid = %s AND tocurrencyid = %s
                )
                """
                result = fetch_one(exchange_rate_query, (bond_currency_id, base_currency_id, bond_currency_id, base_currency_id))
                bond['exchange_rate_to_base'] = result[0] if result else 1.0
        else:
            bond['exchange_rate_to_base'] = 1.0
    
    currencies = get_all_currencies()
    categories = get_all_categories()
    return render_template('securityoverview.html', bonds=bonds, currencies=currencies, categories=categories, base_currency=base_currency)

@admin_bp.route('/securityview_admin/<int:bond_id>')
@admin_required
def securityview_admin(bond_id):
    bond = get_full_bond(bond_id)
    currencies = get_all_currencies()
    categories = get_all_categories()
    return render_template('securityview_admin.html', bond=bond, currencies=currencies, categories=categories)

@admin_bp.route('/create_security', methods=['POST'])
@admin_required
def create_security():
    
    try:
        # Get and validate form data
        bondname = request.form.get('name', '').strip()
        bondsymbol = request.form.get('bondsymbol', '').strip()
        bondcategoryid = request.form.get('bondcategoryid', '').strip()
        bondcurrencyid = request.form.get('bondcurrencyid', '').strip()
        bondcountry = request.form.get('bondcountry', '').strip()
        bondwebsite = request.form.get('bondwebsite', '').strip()
        bondindustry = request.form.get('bondindustry', '').strip()
        bondsector = request.form.get('bondsector', '').strip()
        bonddescription = request.form.get('bonddescription', '').strip()
        
        # Input validation
        if not bondname:
            flash("Security name is required.", "danger")
            return redirect(url_for('admin.securityoverview'))
        
        if not bondsymbol:
            flash("Security symbol is required.", "danger")
            return redirect(url_for('admin.securityoverview'))
        
        if not bondcategoryid or not bondcategoryid.isdigit():
            flash("Valid bond category is required.", "danger")
            return redirect(url_for('admin.securityoverview'))
        
        if not bondcurrencyid or not bondcurrencyid.isdigit():
            flash("Valid currency is required.", "danger")
            return redirect(url_for('admin.securityoverview'))
        
        if not bondsector:
            flash("Sector is required.", "danger")
            return redirect(url_for('admin.securityoverview'))
        
        # Check if bond already exists
        existing_bond = fetch_one("SELECT bondid FROM bond WHERE bondsymbol = %s", (bondsymbol,))
        if existing_bond:
            flash(f"Security {bondsymbol} already exists", 'warning')
            return redirect(url_for('admin.securityoverview'))
        
        # Get exchange information
        bondexchange = get_exchange(bondsymbol)
        if not bondexchange or bondexchange == "Unknown":
            flash(f"Could not determine exchange for {bondsymbol}. Please add the exchange manually.", "warning")
            return redirect(url_for('admin.securityoverview'))
        
        # Get sector ID
        sector_data = fetch_one("SELECT sectorid FROM sector WHERE sectorname = %s", (bondsector,), dictionary=True)
        if not sector_data:
            flash("Invalid sector selected.", "danger")
            return redirect(url_for('admin.securityoverview'))
        bondsectorid = sector_data["sectorid"]
        
        # Get exchange ID
        bondexchangeid = fetch_all("SELECT exchangeid FROM exchange WHERE exchangesymbol = %s", (bondexchange,), dictionary=True)
        if not bondexchangeid:
            regions = fetch_all("SELECT regionid, region FROM region", dictionary=True)
            google_search_url = f"https://www.google.com/search?q={bondsymbol}+stock+exchange+region"
            
            session["pending_bond"] = {
                "bondname": bondname,
                "bondsymbol": bondsymbol,
                "bondcategoryid": bondcategoryid,
                "bondcurrencyid": bondcurrencyid,
                "bondcountry": bondcountry,
                "bondexchange": bondexchange,
                "bondwebsite": bondwebsite,
                "bondindustry": bondindustry,
                "bondsectorid": bondsectorid,
                "bonddescription": bonddescription
            }
            
            return render_template(
                'add_exchange.html', 
                bondsymbol=bondsymbol, 
                regions=regions,
                google_search_url=google_search_url,
                bondname=bondname,
                bondexchangesymbol=bondexchange
            )
        else:
            bondexchangeid = bondexchangeid[0]['exchangeid']

        # Create the bond
        query = """INSERT INTO bond (bondname, bondsymbol, bondcategoryid, bondcurrencyid, bondcountry, bondexchangeid, bondwebsite, bondindustry, bondsectorid, bonddescription) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        execute_change_query(query, (bondname, bondsymbol, bondcategoryid, bondcurrencyid, bondcountry, bondexchangeid, bondwebsite, bondindustry, bondsectorid, bonddescription))
        flash(f"Security {bondsymbol} successfully created", 'success')

        # Get bond data and add initial price
        bondid = fetch_one("SELECT bondid FROM bond WHERE bondsymbol = %s", (bondsymbol,), dictionary=True)
        if bondid:
            bondid = bondid['bondid']
            bondrate, trade_date = get_eod(bondsymbol)
            
            if bondrate and trade_date:
                existing_data = fetch_one("SELECT bondid FROM bonddata WHERE bondid = %s AND bonddatalogtime = %s", (bondid, trade_date))
                if not existing_data:
                    query = "INSERT INTO bonddata (bondid, bonddatalogtime, bondrate) VALUES (%s, %s, %s)"
                    execute_change_query(query, (bondid, trade_date, bondrate))

        execute_change_query("UPDATE status SET securities = %s WHERE id = 1", (date.today(),))
        
    except Exception as e:
        flash(f"An error occurred while creating the security: {str(e)}", "danger")
    
    return redirect(url_for('admin.securityoverview'))

@admin_bp.route('/edit_security/<int:bondid>', methods=['POST'])
@admin_required
def edit_security(bondid):

    name = request.form['name']
    symbol = request.form['bondsymbol']
    categoryid = request.form['bondcategoryid']
    currencyid = request.form['bondcurrencyid']
    country = request.form.get('bondcountry')
    exchange = get_exchange(symbol)
    exchangeid = fetch_one("""SELECT exchangeid FROM exchange WHERE exchangesymbol = %s""", (exchange,), dictionary=True)['exchangeid']
    website = request.form.get('bondwebsite')
    industry = request.form.get('bondindustry')
    sector = request.form.get('bondsectorid')
    description = request.form['bonddescription']

    execute_change_query("""
            UPDATE bond SET
              bondname = %s,
              bondsymbol = %s,
              bondcategoryid = %s,
              bondcurrencyid = %s,
              bondcountry = %s,
              bondexchangeid = %s,
              bondwebsite = %s,
              bondindustry = %s,
              bondsectorid = %s,
              bonddescription = %s
            WHERE bondid = %s
        """, (name, symbol, categoryid, currencyid, country, exchangeid, website, industry, sector, description, bondid))
    
    flash(f"Security {symbol} successfully updated", "success")

    return redirect(url_for('admin.securityview_admin', bond_id=bondid))

@admin_bp.route('/delete_security/<int:bondid>', methods=['POST'])
@admin_required
def delete_security(bondid):
    bondsymbol = fetch_one("SELECT bondsymbol FROM bond WHERE bondid = %s", (bondid,), dictionary=True)['bondsymbol']
    execute_change_query("""DELETE FROM bond WHERE bondid = %s""", (bondid,))
    flash(f"Security {bondsymbol} successfully deleted", 'success')
    return redirect(url_for('admin.securityoverview'))

@admin_bp.route('/currencyoverview')
@admin_required
def currencyoverview():
    currencies = get_all_currencies()
    return render_template('currencyoverview.html', currencies=currencies)

@admin_bp.route('/create_currency', methods=['POST'])
@admin_required
def create_currency():

    currencycode = request.form.get('currencycode')
    currencyname = request.form.get('currencyname')

    existing_currency = fetch_one("""SELECT currencyid FROM currency WHERE currencycode = %s""", (currencycode,))
    if existing_currency:
        flash(f"Currency {currencycode} does exist alredy", "danger")
        return redirect(url_for('admin.currencyoverview'))
    else:
        query = """INSERT INTO currency (currencycode, currencyname) VALUES (%s, %s)"""
        execute_change_query(query, (currencycode, currencyname))
    
    fetch_daily_exchangerates()  # Update exchange rates after adding a new currency

    flash(f"Currency {currencycode} successfully created", "success")

    return redirect(url_for('admin.currencyoverview'))

@admin_bp.route('/delete_currency/<int:currencyid>', methods=['POST'])
@admin_required
def delete_currency(currencyid):
    currencycode = fetch_one("""SELECT currencycode FROM currency WHERE currencyid = %s""", (currencyid,), dictionary=True)['currencycode']
    try:
        execute_change_query("""DELETE FROM currency WHERE currencyid = %s""", (currencyid,))
        flash(f"Currency {currencycode} has been successfully deleted", "success")
    except mysql.connector.errors.IntegrityError as e:
        flash(f"Cannot delete Currency {currencycode} because its referenced in other records.", "danger")
    return redirect(url_for('admin.currencyoverview'))


@admin_bp.route('/useroverview')
@admin_required
def useroverview():
    users = get_all_users()
    return render_template('useroverview.html', users=users)


@admin_bp.route('/delete_user/<int:userid>', methods=['POST'])
@admin_required
def delete_user(userid):
    if userid == 1:
        flash('Cannot delete the admin user.', 'danger')
        return redirect(url_for('admin.useroverview'))
    username = fetch_one("""SELECT username FROM user where userid = %s""", (userid,), dictionary=True)['username']
    execute_change_query("""DELETE FROM user WHERE userid = %s""", (userid,))
    flash(f"User {username} has been successfully deleted", "success")
    return redirect(url_for('admin.useroverview'))


@admin_bp.route('/edit_user/<int:userid>', methods=['POST'])
@admin_required
def edit_user(userid):

    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin')

    if userid == 1:
        flash('Cannot edit the admin user.', 'danger')
        return redirect(url_for('admin.useroverview'))
    
    newnameid = fetch_one("""SELECT userid FROM user where username = %s""", (username,), dictionary=True)
    if newnameid is not None:
        newnameid = newnameid['userid']
        if newnameid != userid:
            flash(f"Username {username} is already taken", "danger")
            return redirect(url_for('admin.useroverview'))

    if password:
        password = generate_password_hash(password)
    else:
        existing_user = fetch_one("""SELECT userpwd FROM user WHERE userid = %s""", (userid,), dictionary=True)
        password = existing_user['userpwd'] if existing_user else None
    is_admin = True if is_admin == '1' else False

    execute_change_query("""
        UPDATE user SET
          username = %s,
          userpwd = %s,
          is_admin = %s
        WHERE userid = %s
    """, (username, password, is_admin, userid))

    flash(f"Details for User {username} have been successfully updated", "success")

    return redirect(url_for('admin.useroverview'))

@admin_bp.route('/create_user', methods=['POST'])
@admin_required
def create_user():

    username = request.form.get('username')
    password = request.form.get('password')
    password_confirm = request.form.get('passwordconfirm')
    is_admin = request.form.get('is_admin')

    existing_user = fetch_one("""SELECT username FROM user where username = %s""", (username,))

    if existing_user:
        flash(f"Username {username} is already taken", "danger")
        return redirect(url_for('admin.useroverview'))

    if password != password_confirm:
        flash('Passwords do not match.', 'danger')
        return redirect(url_for('admin.useroverview'))
    
    password_hashed = generate_password_hash(password)
    is_admin_bool = True if is_admin == 'on' else False

    execute_change_query("""
        INSERT INTO user (username, userpwd, is_admin)
        VALUES (%s, %s, %s)
    """, (username, password_hashed, is_admin_bool))

    flash(f'User {username } has been successfully created.', 'success')
    return redirect(url_for('admin.useroverview'))

@admin_bp.route('/exchangeoverview', strict_slashes=False)
@admin_required
def exchangeoverview():
    exchanges = fetch_all("""SELECT exchangeid, exchangesymbol, r.region, r.regionid FROM exchange JOIN region r ON exchange.region = r.regionid""", dictionary=True)
    regions = fetch_all("""SELECT * FROM region""", dictionary=True)
    return render_template('exchangeoverview.html', exchanges=exchanges, regions=regions)

@admin_bp.route('/create_exchange', methods=['POST'])
@admin_required
def create_exchange():
    exchangesymbol = request.form.get("exchangesymbol")
    regionid = request.form.get("region")

    if not exchangesymbol or not regionid:
        flash("Exchange symbol and region are required.", "danger")
        return redirect(url_for("admin.exchangeoverview"))
    
    existing_exchange = fetch_one("""SELECT exchangeid FROM exchange WHERE exchangesymbol = %s""", (exchangesymbol,))
    if existing_exchange:
        flash(f"Exchange {exchangesymbol} already exists.", "warning")
        return redirect(url_for("admin.exchangeoverview"))
    
    execute_change_query(
        "INSERT INTO exchange (exchangesymbol, region) VALUES (%s, %s)",
        (exchangesymbol, regionid)
    )
    flash(f"Exchange {exchangesymbol} created successfully.", "success")
    return redirect(url_for('admin.exchangeoverview'))

@admin_bp.route('/edit_exchange/<int:exchangeid>', methods=['POST'])
@admin_required
def edit_exchange(exchangeid):
    new_region = request.form.get('region')
        # Update the exchange in the database
    execute_change_query(
        "UPDATE exchange SET region = %s WHERE exchangeid = %s",
        (new_region, exchangeid)
    )
    regionsymbol = fetch_one("SELECT exchangesymbol FROM exchange WHERE exchangeid = %s", (exchangeid,), dictionary=True)['exchangesymbol']
    flash(f"Exchange {regionsymbol} updated successfully.", "success")
    return redirect(url_for('admin.exchangeoverview'))

@admin_bp.route('/delete_exchange/<int:exchangeid>', methods=['POST'])
@admin_required
def delete_exchange(exchangeid):
    exchange = fetch_one("""SELECT exchangesymbol FROM exchange where exchangeid = %s""", (exchangeid,), dictionary=True)['exchangesymbol']
    try:
        execute_change_query("""DELETE FROM exchange WHERE exchangeid = %s""", (exchangeid,))
        flash(f"Exchange {exchange} has been successfully deleted", "success")
    except mysql.connector.errors.IntegrityError as e:
        flash(f"Cannot delete Exchange {exchange} because its referenced in other records.", "danger")
    return redirect(url_for('admin.currencyoverview'))

@admin_bp.route('/create_security_continued', methods=['POST'])
@admin_required
def create_security_continued():
    
    try:
        exchangesymbol = request.form.get("exchangesymbol", "").strip()
        regionid = request.form.get("region", "").strip()
        
        # Input validation
        if not exchangesymbol or not regionid:
            flash("Exchange symbol and region are required.", "danger")
            return redirect(url_for("admin.securityoverview"))
        
        if not regionid.isdigit():
            flash("Invalid region selected.", "danger")
            return redirect(url_for("admin.securityoverview"))
        
        # Check if exchange already exists
        existing_exchange = fetch_one("""SELECT exchangeid FROM exchange WHERE exchangesymbol = %s""", (exchangesymbol,))
        if existing_exchange:
            flash(f"Exchange {exchangesymbol} already exists.", "warning")
            return redirect(url_for("admin.securityoverview"))
        
        # Create new exchange
        execute_change_query(
            "INSERT INTO exchange (exchangesymbol, region) VALUES (%s, %s)",
            (exchangesymbol, int(regionid))
        )

        pending_bond = session.get("pending_bond")
        if not pending_bond:
            flash("No pending security creation found.", "danger")
            return redirect(url_for("admin.securityoverview"))
        
        # Get the newly created exchange ID
        bondexchangeid = fetch_one("""SELECT exchangeid FROM exchange WHERE exchangesymbol = %s""", (exchangesymbol,), dictionary=True)
        if not bondexchangeid:
            flash("Failed to create exchange.", "danger")
            return redirect(url_for("admin.securityoverview"))
        
        bondexchangeid = bondexchangeid['exchangeid']
        
        # Check if bond already exists
        existing_bond = fetch_one("""SELECT bondid FROM bond WHERE bondsymbol = %s""", (pending_bond['bondsymbol'],))
        if existing_bond:
            flash(f"Security {pending_bond['bondsymbol']} already exists", "warning")
            session.pop("pending_bond", None)
            return redirect(url_for("admin.securityoverview"))
        
        # Create the bond
        query = """INSERT INTO bond 
            (bondname, bondsymbol, bondcategoryid, bondcurrencyid, bondcountry, bondexchangeid, bondwebsite, bondindustry, bondsectorid, bonddescription) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        execute_change_query(query, (
            pending_bond["bondname"],
            pending_bond["bondsymbol"],
            pending_bond["bondcategoryid"],
            pending_bond["bondcurrencyid"],
            pending_bond["bondcountry"],
            bondexchangeid,
            pending_bond["bondwebsite"],
            pending_bond["bondindustry"],
            pending_bond["bondsectorid"],
            pending_bond["bonddescription"]
        ))

        # Clean up session after successful insert
        session.pop("pending_bond", None)

        flash(f"Exchange {exchangesymbol} and Security {pending_bond['bondsymbol']} successfully added.", "success")
        return redirect(url_for("admin.securityoverview"))
        
    except Exception as e:
        flash(f"An error occurred while creating the security: {str(e)}", "danger")
        return redirect(url_for("admin.securityoverview"))