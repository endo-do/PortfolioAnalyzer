# Admin routes for Portfolio Analyzer - manages securities, currencies, users, exchanges, and API operations with comprehensive logging
"""Admin routes for managing securities, currencies, and users."""

from datetime import date
from flask import render_template, url_for, redirect, request, flash, session, jsonify
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
    from app.utils.currency_utils import get_user_default_currency
    base_currency = get_user_default_currency(current_user)
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
    exchanges = fetch_all("""SELECT exchangeid, exchangename, r.region, r.regionid FROM exchange JOIN region r ON exchange.region = r.regionid ORDER BY exchangename""", dictionary=True)
    regions = fetch_all("""SELECT * FROM region""", dictionary=True)
    sectors = fetch_all("""SELECT sectorid as id, sectorname, sectordisplayname FROM sector""", dictionary=True)
    return render_template('securityoverview.html', bonds=bonds, currencies=currencies, categories=categories, exchanges=exchanges, regions=regions, sectors=sectors, base_currency=base_currency)

@admin_bp.route('/securityview_admin/<int:bond_id>')
@admin_required
def securityview_admin(bond_id):
    bond = get_full_bond(bond_id)
    currencies = get_all_currencies()
    categories = get_all_categories()
    exchanges = fetch_all("""SELECT exchangeid, exchangename, r.region, r.regionid FROM exchange JOIN region r ON exchange.region = r.regionid ORDER BY exchangename""", dictionary=True)
    regions = fetch_all("""SELECT * FROM region""", dictionary=True)
    sectors = fetch_all("""SELECT sectorid as id, sectorname, sectordisplayname FROM sector""", dictionary=True)
    return render_template('securityview_admin.html', bond=bond, currencies=currencies, categories=categories, exchanges=exchanges, regions=regions, sectors=sectors)

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
        bondsectorid = request.form.get('bondsectorid', '').strip()
        bonddescription = request.form.get('bonddescription', '').strip()
        
        # Input validation
        if not bondname:
            return jsonify({"status": "error", "message": "Security name is required"})
        
        if not bondsymbol:
            return jsonify({"status": "error", "message": "Security symbol is required"})
        
        if not bondcategoryid or not bondcategoryid.isdigit():
            return jsonify({"status": "error", "message": "Valid bond category is required"})
        
        if not bondcurrencyid:
            return jsonify({"status": "error", "message": "Valid currency is required"})
        
        # Check if bond already exists BEFORE handling currency/exchange creation
        existing_bond = fetch_one("SELECT bondid FROM bond WHERE bondsymbol = %s", (bondsymbol,))
        if existing_bond:
            return jsonify({"status": "error", "message": f"Security '{bondsymbol}' already exists. Please use a different symbol or check if the security is already in the system."})
        
        # Validate that currency is a valid ID
        if not bondcurrencyid.isdigit():
            return jsonify({"status": "error", "message": "Valid currency is required"})
        
        if not bondsectorid or not bondsectorid.isdigit():
            return jsonify({"status": "error", "message": "Valid sector is required"})
        
        # Validate that the sector ID exists in the database
        sector_data = fetch_one("SELECT sectorid FROM sector WHERE sectorid = %s", (bondsectorid,), dictionary=True)
        if not sector_data:
            return jsonify({"status": "error", "message": "Invalid sector selected"})

        # Create the bond (without exchange)
        query = """INSERT INTO bond (bondname, bondsymbol, bondcategoryid, bondcurrencyid, bondcountry, bondwebsite, bondindustry, bondsectorid, bonddescription) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        execute_change_query(query, (bondname, bondsymbol, bondcategoryid, bondcurrencyid, bondcountry, bondwebsite, bondindustry, bondsectorid, bonddescription))

        # Get bond data and add initial price
        bondid = fetch_one("SELECT bondid FROM bond WHERE bondsymbol = %s", (bondsymbol,), dictionary=True)
        if bondid:
            bondid = bondid['bondid']
            bondrate, volume, trade_date = get_eod(bondsymbol)
            
            if bondrate and trade_date:
                existing_data = fetch_one("SELECT bondid FROM bonddata WHERE bondid = %s AND bonddatalogtime = %s", (bondid, trade_date))
                if not existing_data:
                    query = "INSERT INTO bonddata (bondid, bonddatalogtime, bondrate, bondvolume) VALUES (%s, %s, %s, %s)"
                    execute_change_query(query, (bondid, trade_date, bondrate, volume))

        execute_change_query("UPDATE status SET securities = %s WHERE id = 1", (date.today(),))
        
        return jsonify({"status": "success", "message": f"Security {bondsymbol} successfully created"})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@admin_bp.route('/edit_security/<int:bondid>', methods=['POST'])
@admin_required
def edit_security(bondid):

    name = request.form['name']
    symbol = request.form['bondsymbol']
    categoryid = request.form['bondcategoryid']
    currencyid = request.form['bondcurrencyid']
    country = request.form.get('bondcountry')
    exchangeid = request.form.get('bondexchangeid')
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
        INSERT INTO user (username, userpwd, email, default_base_currency, is_admin)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, password_hashed, 'N/A', 1, is_admin_bool))

    flash(f'User {username } has been successfully created.', 'success')
    return redirect(url_for('admin.useroverview'))

@admin_bp.route('/exchangeoverview', strict_slashes=False)
@admin_required
def exchangeoverview():
    exchanges = fetch_all("""SELECT exchangeid, exchangename, r.region, r.regionid FROM exchange JOIN region r ON exchange.region = r.regionid""", dictionary=True)
    regions = fetch_all("""SELECT * FROM region""", dictionary=True)
    return render_template('exchangeoverview.html', exchanges=exchanges, regions=regions)

@admin_bp.route('/create_exchange', methods=['POST'])
@admin_required
def create_exchange():
    exchangename = request.form.get("exchangename")
    regionid = request.form.get("region")

    if not exchangename or not regionid:
        flash("Exchange name and region are required.", "danger")
        return redirect(url_for("admin.exchangeoverview"))
    
    existing_exchange = fetch_one("""SELECT exchangeid FROM exchange WHERE exchangename = %s""", (exchangename,))
    if existing_exchange:
        flash(f"Exchange {exchangename} already exists.", "warning")
        return redirect(url_for("admin.exchangeoverview"))
    
    execute_change_query(
        "INSERT INTO exchange (exchangename, region) VALUES (%s, %s)",
        (exchangename, regionid)
    )
    flash(f"Exchange {exchangename} created successfully.", "success")
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
    regionsymbol = fetch_one("SELECT exchangename FROM exchange WHERE exchangeid = %s", (exchangeid,), dictionary=True)['exchangename']
    flash(f"Exchange {regionsymbol} updated successfully.", "success")
    return redirect(url_for('admin.exchangeoverview'))

@admin_bp.route('/delete_exchange/<int:exchangeid>', methods=['POST'])
@admin_required
def delete_exchange(exchangeid):
    exchange = fetch_one("""SELECT exchangename FROM exchange where exchangeid = %s""", (exchangeid,), dictionary=True)['exchangename']
    try:
        execute_change_query("""DELETE FROM exchange WHERE exchangeid = %s""", (exchangeid,))
        flash(f"Exchange {exchange} has been successfully deleted", "success")
    except mysql.connector.errors.IntegrityError as e:
        flash(f"Cannot delete Exchange {exchange} because its referenced in other records.", "danger")
    return redirect(url_for('admin.exchangeoverview'))

@admin_bp.route('/create_security_continued', methods=['POST'])
@admin_required
def create_security_continued():
    
    try:
        exchangename = request.form.get("exchangename", "").strip()
        regionid = request.form.get("region", "").strip()
        
        # Input validation
        if not exchangename or not regionid:
            flash("Exchange name and region are required.", "danger")
            return redirect(url_for("admin.securityoverview"))
        
        if not regionid.isdigit():
            flash("Invalid region selected.", "danger")
            return redirect(url_for("admin.securityoverview"))
        
        # Check if exchange already exists
        existing_exchange = fetch_one("""SELECT exchangeid FROM exchange WHERE exchangename = %s""", (exchangename,))
        if existing_exchange:
            flash(f"Exchange {exchangename} already exists.", "warning")
            return redirect(url_for("admin.securityoverview"))
        
        # Create new exchange
        execute_change_query(
            "INSERT INTO exchange (exchangename, region) VALUES (%s, %s)",
            (exchangename, int(regionid))
        )

        pending_bond = session.get("pending_bond")
        if not pending_bond:
            flash("No pending security creation found.", "danger")
            return redirect(url_for("admin.securityoverview"))
        
        # Get the newly created exchange ID
        bondexchangeid = fetch_one("""SELECT exchangeid FROM exchange WHERE exchangename = %s""", (exchangename,), dictionary=True)
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

        flash(f"Exchange {exchangename} and Security {pending_bond['bondsymbol']} successfully added.", "success")
        return redirect(url_for("admin.securityoverview"))
        
    except Exception as e:
        flash(f"An error occurred while creating the security: {str(e)}", "danger")
        return redirect(url_for("admin.securityoverview"))

@admin_bp.route('/check_security_exists', methods=['POST'])
@admin_required
def check_security_exists():
    try:
        bondsymbol = request.form.get('bondsymbol', '').strip()
        
        if not bondsymbol:
            return jsonify({"exists": False})
        
        # Check if bond already exists
        existing_bond = fetch_one("SELECT bondid FROM bond WHERE bondsymbol = %s", (bondsymbol,))
        
        return jsonify({"exists": existing_bond is not None})
        
    except Exception as e:
        return jsonify({"exists": False, "error": str(e)})

@admin_bp.route('/create_currency_ajax', methods=['POST'])
@admin_required
def create_currency_ajax():
    try:
        currencycode = request.form.get('currencycode', '').strip().upper()
        currencyname = request.form.get('currencyname', '').strip()
        
        if not currencycode or len(currencycode) != 3:
            return jsonify({"status": "error", "message": "Currency code must be 3 characters long"})
        
        if not currencyname:
            return jsonify({"status": "error", "message": "Currency name is required"})
        
        # Check if currency already exists
        existing = fetch_one("SELECT currencyid FROM currency WHERE currencycode = %s", (currencycode,))
        if existing:
            return jsonify({"status": "error", "message": "Currency already exists"})
        
        # Create the currency
        execute_change_query("INSERT INTO currency (currencycode, currencyname) VALUES (%s, %s)", (currencycode, currencyname))
        
        # Update exchange rates after adding a new currency
        from app.database.tables.exchangerate.fetch_daily_exchangerates import fetch_daily_exchangerates
        fetch_daily_exchangerates()
        
        # Get the new currency ID
        new_currency = fetch_one("SELECT currencyid FROM currency WHERE currencycode = %s", (currencycode,), dictionary=True)
        
        return jsonify({
            "status": "success", 
            "currency_id": new_currency["currencyid"],
            "currency_code": currencycode
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@admin_bp.route('/api_management')
@admin_required
def api_management():
    """API Management dashboard showing fetch logs and manual controls."""
    try:
        # Check if api_fetch_logs table exists
        table_exists = fetch_one("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'portfolioanalyzer' 
            AND table_name = 'api_fetch_logs'
        """)
        
        if not table_exists or table_exists[0] == 0:
            # Table doesn't exist, create it
            from app.database.tables.api_fetch_logs.add_api_fetch_logs_table import add_api_fetch_logs_table
            if not add_api_fetch_logs_table():
                flash('Failed to create API fetch logs table.', 'danger')
                return render_template('api_management.html', 
                                     recent_fetches=[], 
                                     failed_fetches=[], 
                                     api_stats={})
        
        # Get recent API fetch logs (last 50) - exclude individual failed fetches
        recent_fetches = fetch_all("""
            SELECT 
                afl.id,
                afl.symbol,
                afl.fetch_type,
                afl.status,
                afl.error_message,
                afl.fetch_time,
                afl.retry_count
            FROM api_fetch_logs afl
            WHERE NOT (afl.status = 'FAILED' AND afl.symbol NOT IN ('STOCK_FETCH_BULK', 'EXCHANGE_FETCH_BULK'))
            ORDER BY afl.fetch_time DESC
            LIMIT 50
        """, dictionary=True)
        
        # Get failed fetches
        failed_fetches = fetch_all("""
            SELECT 
                afl.id,
                afl.symbol,
                afl.fetch_type,
                afl.error_message,
                afl.fetch_time,
                afl.retry_count
            FROM api_fetch_logs afl
            WHERE afl.status = 'FAILED'
            ORDER BY afl.fetch_time DESC
            LIMIT 20
        """, dictionary=True)
        
        # Get API statistics
        api_stats = fetch_one("""
            SELECT 
                COUNT(*) as total_fetches,
                SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) as successful_fetches,
                SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) as failed_fetches,
                MAX(fetch_time) as last_fetch
            FROM api_fetch_logs
            WHERE fetch_time >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
        """, dictionary=True)
        
        return render_template('api_management.html', 
                             recent_fetches=recent_fetches or [],
                             failed_fetches=failed_fetches or [],
                             api_stats=api_stats or {})
        
    except Exception as e:
        log_error(e, {'action': 'api_management', 'user_id': current_user.id})
        flash('Error loading API management data: ' + str(e), 'danger')
        return render_template('api_management.html', 
                             recent_fetches=[], 
                             failed_fetches=[], 
                             api_stats={})

@admin_bp.route('/manual_fetch_stocks', methods=['POST'])
@admin_required
def manual_fetch_stocks():
    """Manually trigger stock price fetch."""
    try:
        from app.database.tables.bond.fetch_daily_securityrates import fetch_daily_securityrates
        from app.database.helpers.execute_change_query import execute_change_query
        from datetime import date
        
        # Log the manual fetch attempt
        log_user_action('MANUAL_STOCK_FETCH', {
            'user_id': current_user.id,
            'action': 'manual_stock_fetch'
        })
        
        # Force fetch by temporarily resetting the status
        execute_change_query("UPDATE status SET securities = '1900-01-01' WHERE id = 1")
        
        # Execute the fetch
        fetch_daily_securityrates()
        
        flash('Stock prices fetched successfully!', 'success')
        return redirect(url_for('admin.api_management'))
        
    except Exception as e:
        log_error(e, {'action': 'manual_fetch_stocks', 'user_id': current_user.id})
        flash('Error fetching stock prices: ' + str(e), 'danger')
        return redirect(url_for('admin.api_management'))

@admin_bp.route('/manual_fetch_exchange_rates', methods=['POST'])
@admin_required
def manual_fetch_exchange_rates():
    """Manually trigger exchange rate fetch."""
    try:
        from app.database.tables.exchangerate.fetch_daily_exchangerates import fetch_daily_exchangerates
        from app.database.helpers.execute_change_query import execute_change_query
        from datetime import date
        
        # Log the manual fetch attempt
        log_user_action('MANUAL_EXCHANGE_FETCH', {
            'user_id': current_user.id,
            'action': 'manual_exchange_fetch'
        })
        
        # Force fetch by temporarily resetting the status
        execute_change_query("UPDATE status SET exchangerates = '1900-01-01' WHERE id = 1")
        
        # Execute the fetch
        fetch_daily_exchangerates()
        
        flash('Exchange rates fetched successfully!', 'success')
        return redirect(url_for('admin.api_management'))
        
    except Exception as e:
        log_error(e, {'action': 'manual_fetch_exchange_rates', 'user_id': current_user.id})
        flash('Error fetching exchange rates: ' + str(e), 'danger')
        return redirect(url_for('admin.api_management'))

@admin_bp.route('/fetch_single_security', methods=['POST'])
@admin_required
def fetch_single_security():
    """Fetch a single security by symbol."""
    try:
        symbol = request.form.get('symbol', '').strip().upper()
        
        if not symbol:
            flash('Symbol is required.', 'danger')
            return redirect(url_for('admin.api_management'))
        
        from app.api.get_eod import get_eod
        from app.database.helpers.fetch_one import fetch_one
        from app.database.helpers.execute_change_query import execute_change_query
        from app.database.tables.bonddata.bonddata_exists import bonddata_exists
        from app.api.get_last_trading_day import get_last_trading_day
        
        # Log the manual fetch attempt
        log_user_action('MANUAL_SINGLE_SECURITY_FETCH', {
            'user_id': current_user.id,
            'symbol': symbol
        })
        
        # Fetch the data
        price, volume, trade_date = get_eod(symbol)
        
        if price is not None and trade_date is not None:
            # Get bond ID
            bond_id = fetch_one("SELECT bondid FROM bond WHERE bondsymbol = %s", (symbol,))
            if bond_id:
                bond_id = bond_id[0]
                
                # Insert or update the data
                if bonddata_exists(bond_id, log_date=trade_date):
                    execute_change_query("""
                        UPDATE bonddata
                        SET bondrate = %s, bondvolume = %s
                        WHERE bondid = %s AND bonddatalogtime = %s
                    """, (price, volume, bond_id, trade_date))
                else:
                    execute_change_query("""
                        INSERT INTO bonddata (bondid, bondrate, bondvolume, bonddatalogtime)
                        VALUES (%s, %s, %s, %s)
                    """, (bond_id, price, volume, trade_date))
                
                # Log successful individual fetch
                try:
                    from app.database.tables.api_fetch_logs.log_api_fetch import log_api_fetch
                    log_api_fetch(symbol, 'STOCK', 'SUCCESS', f'Successfully fetched {symbol}: {price:.2f}')
                except:
                    pass
                
                flash(f'Successfully fetched {symbol}: {price:.2f}', 'success')
            else:
                # Log failure - security not found
                try:
                    from app.database.tables.api_fetch_logs.log_api_fetch import log_api_fetch
                    log_api_fetch(symbol, 'STOCK', 'FAILED', f'Security {symbol} not found in database')
                except:
                    pass
                flash(f'Security {symbol} not found in database.', 'warning')
        else:
            # Log failure - no data available
            try:
                from app.database.tables.api_fetch_logs.log_api_fetch import log_api_fetch
                log_api_fetch(symbol, 'STOCK', 'FAILED', f'No data available for {symbol}')
            except:
                pass
            flash(f'No data available for {symbol}', 'warning')
        
        return redirect(url_for('admin.api_management'))
        
    except Exception as e:
        log_error(e, {'action': 'fetch_single_security', 'user_id': current_user.id, 'symbol': symbol})
        flash(f'Error fetching {symbol}: {str(e)}', 'danger')
        return redirect(url_for('admin.api_management'))

@admin_bp.route('/fetch_single_exchange_rate', methods=['POST'])
@admin_required
def fetch_single_exchange_rate():
    """Fetch a single exchange rate by pair."""
    try:
        pair = request.form.get('pair', '').strip().upper()
        
        if not pair or len(pair) != 6:
            flash('Exchange rate pair must be 6 characters (e.g., USDCHF).', 'danger')
            return redirect(url_for('admin.api_management'))
        
        from app.api.get_exchange_matrix import get_exchange_matrix
        from app.database.tables.currency.get_currency_id_by_code import get_currency_id_by_code
        from app.database.helpers.execute_change_query import execute_change_query
        from app.database.tables.exchangerate.exchange_rate_exists import exchange_rate_exists
        from app.api.get_last_trading_day import get_last_trading_day
        
        # Log the manual fetch attempt
        log_user_action('MANUAL_SINGLE_EXCHANGE_FETCH', {
            'user_id': current_user.id,
            'pair': pair
        })
        
        # Extract currencies
        from_currency = pair[:3]
        to_currency = pair[3:]
        
        # Fetch the exchange rate
        exchange_rates = get_exchange_matrix([from_currency, to_currency])
        rate = exchange_rates.get(pair)
        
        if rate is not None:
            from_id = get_currency_id_by_code(from_currency)
            to_id = get_currency_id_by_code(to_currency)
            
            if from_id and to_id:
                trading_day = get_last_trading_day()
                
                # Fallback to current date if get_last_trading_day() returns None
                if trading_day is None:
                    from datetime import date
                    trading_day = date.today().strftime("%Y-%m-%d")
                
                # Insert or update the exchange rate
                if exchange_rate_exists(from_id, to_id, log_date=trading_day):
                    execute_change_query("""
                        UPDATE exchangerate
                        SET exchangerate = %s
                        WHERE fromcurrencyid = %s AND tocurrencyid = %s AND exchangeratelogtime = %s
                    """, (rate, from_id, to_id, trading_day))
                else:
                    execute_change_query("""
                        INSERT INTO exchangerate (fromcurrencyid, tocurrencyid, exchangerate, exchangeratelogtime)
                        VALUES (%s, %s, %s, %s)
                    """, (from_id, to_id, rate, trading_day))
                
                # Log successful individual fetch
                try:
                    from app.database.tables.api_fetch_logs.log_api_fetch import log_api_fetch
                    log_api_fetch(pair, 'EXCHANGE', 'SUCCESS', f'Successfully fetched {pair}: {rate:.4f}')
                except:
                    pass
                
                flash(f'Successfully fetched {pair}: {rate:.4f}', 'success')
            else:
                # Log failure - currency pair not found
                try:
                    from app.database.tables.api_fetch_logs.log_api_fetch import log_api_fetch
                    log_api_fetch(pair, 'EXCHANGE', 'FAILED', f'Currency pair {pair} not found in database')
                except:
                    pass
                flash(f'Currency pair {pair} not found in database.', 'warning')
        else:
            # Log failure - no data available
            try:
                from app.database.tables.api_fetch_logs.log_api_fetch import log_api_fetch
                log_api_fetch(pair, 'EXCHANGE', 'FAILED', f'No exchange rate data available for {pair}')
            except:
                pass
            flash(f'No exchange rate data available for {pair}', 'warning')
        
        return redirect(url_for('admin.api_management'))
        
    except Exception as e:
        log_error(e, {'action': 'fetch_single_exchange_rate', 'user_id': current_user.id, 'pair': pair})
        flash(f'Error fetching {pair}: {str(e)}', 'danger')
        return redirect(url_for('admin.api_management'))

@admin_bp.route('/retry_failed_fetch/<int:fetch_id>', methods=['POST'])
@admin_required
def retry_failed_fetch(fetch_id):
    """Retry a failed API fetch."""
    try:
        # Get the failed fetch details
        fetch_details = fetch_one("""
            SELECT symbol, fetch_type, retry_count
            FROM api_fetch_logs
            WHERE id = %s AND status = 'FAILED'
        """, (fetch_id,), dictionary=True)
        
        if not fetch_details:
            flash('Failed fetch not found.', 'danger')
            return redirect(url_for('admin.api_management'))
        
        # Check retry limit (max 3 retries)
        if fetch_details['retry_count'] >= 3:
            flash('Maximum retry attempts reached for this fetch.', 'warning')
            return redirect(url_for('admin.api_management'))
        
        # Log the retry attempt
        log_user_action('RETRY_FAILED_FETCH', {
            'user_id': current_user.id,
            'fetch_id': fetch_id,
            'symbol': fetch_details['symbol'],
            'fetch_type': fetch_details['fetch_type']
        })
        
        # Retry based on fetch type
        if fetch_details['fetch_type'] == 'STOCK':
            from app.api.get_eod import get_eod
            from app.database.tables.bonddata.bonddata_exists import bonddata_exists
            from app.api.get_last_trading_day import get_last_trading_day
            
            price, volume, trade_date = get_eod(fetch_details['symbol'])
            
            if price is not None and trade_date is not None:
                # Get bond ID and update database
                bond_id = fetch_one("SELECT bondid FROM bond WHERE bondsymbol = %s", (fetch_details['symbol'],))
                if bond_id:
                    bond_id = bond_id[0]
                    
                    # Insert or update the data
                    if bonddata_exists(bond_id, log_date=trade_date):
                        execute_change_query("""
                            UPDATE bonddata
                            SET bondrate = %s, bondvolume = %s
                            WHERE bondid = %s AND bonddatalogtime = %s
                        """, (price, volume, bond_id, trade_date))
                    else:
                        execute_change_query("""
                            INSERT INTO bonddata (bondid, bondrate, bondvolume, bonddatalogtime)
                            VALUES (%s, %s, %s, %s)
                        """, (bond_id, price, volume, trade_date))
                    
                    # Update the log as successful
                    execute_change_query("""
                        UPDATE api_fetch_logs 
                        SET status = 'SUCCESS', error_message = NULL, retry_count = retry_count + 1
                        WHERE id = %s
                    """, (fetch_id,))
                    flash(f'Successfully retried fetch for {fetch_details["symbol"]}: {price:.2f}', 'success')
                else:
                    # Update retry count
                    execute_change_query("""
                        UPDATE api_fetch_logs 
                        SET retry_count = retry_count + 1, error_message = 'Retry failed: Security not found in database'
                        WHERE id = %s
                    """, (fetch_id,))
                    flash(f'Retry failed for {fetch_details["symbol"]}: Security not found in database', 'warning')
            else:
                # Update retry count
                execute_change_query("""
                    UPDATE api_fetch_logs 
                    SET retry_count = retry_count + 1, error_message = 'Retry failed: No data available'
                    WHERE id = %s
                """, (fetch_id,))
                flash(f'Retry failed for {fetch_details["symbol"]}: No data available', 'warning')
        
        elif fetch_details['fetch_type'] == 'EXCHANGE':
            from app.api.get_exchange_matrix import get_exchange_matrix
            from app.database.tables.currency.get_currency_id_by_code import get_currency_id_by_code
            from app.database.tables.exchangerate.exchange_rate_exists import exchange_rate_exists
            from app.api.get_last_trading_day import get_last_trading_day
            
            # Extract currencies from pair
            pair = fetch_details['symbol']
            from_currency = pair[:3]
            to_currency = pair[3:]
            
            # Fetch the exchange rate
            exchange_rates = get_exchange_matrix([from_currency, to_currency])
            rate = exchange_rates.get(pair)
            
            if rate is not None:
                from_id = get_currency_id_by_code(from_currency)
                to_id = get_currency_id_by_code(to_currency)
                
                if from_id and to_id:
                    trading_day = get_last_trading_day()
                    
                    # Fallback to current date if get_last_trading_day() returns None
                    if trading_day is None:
                        from datetime import date
                        trading_day = date.today().strftime("%Y-%m-%d")
                    
                    # Insert or update the exchange rate
                    if exchange_rate_exists(from_id, to_id, log_date=trading_day):
                        execute_change_query("""
                            UPDATE exchangerate
                            SET exchangerate = %s
                            WHERE fromcurrencyid = %s AND tocurrencyid = %s AND exchangeratelogtime = %s
                        """, (rate, from_id, to_id, trading_day))
                    else:
                        execute_change_query("""
                            INSERT INTO exchangerate (fromcurrencyid, tocurrencyid, exchangerate, exchangeratelogtime)
                            VALUES (%s, %s, %s, %s)
                        """, (from_id, to_id, rate, trading_day))
                    
                    # Update the log as successful
                    execute_change_query("""
                        UPDATE api_fetch_logs 
                        SET status = 'SUCCESS', error_message = NULL, retry_count = retry_count + 1
                        WHERE id = %s
                    """, (fetch_id,))
                    flash(f'Successfully retried fetch for {pair}: {rate:.4f}', 'success')
                else:
                    # Update retry count
                    execute_change_query("""
                        UPDATE api_fetch_logs 
                        SET retry_count = retry_count + 1, error_message = 'Retry failed: Currency pair not found in database'
                        WHERE id = %s
                    """, (fetch_id,))
                    flash(f'Retry failed for {pair}: Currency pair not found in database', 'warning')
            else:
                # Update retry count
                execute_change_query("""
                    UPDATE api_fetch_logs 
                    SET retry_count = retry_count + 1, error_message = 'Retry failed: No exchange rate data available'
                    WHERE id = %s
                """, (fetch_id,))
                flash(f'Retry failed for {pair}: No exchange rate data available', 'warning')
        
        return redirect(url_for('admin.api_management'))
        
    except Exception as e:
        log_error(e, {'action': 'retry_failed_fetch', 'user_id': current_user.id, 'fetch_id': fetch_id})
        flash('Error retrying fetch: ' + str(e), 'danger')
        return redirect(url_for('admin.api_management'))

@admin_bp.route('/create_exchange_ajax', methods=['POST'])
@admin_required
def create_exchange_ajax():
    try:
        exchangename = request.form.get('exchangename', '').strip().upper()
        regionid = request.form.get('regionid', '').strip()
        
        if not exchangename:
            return jsonify({"status": "error", "message": "Exchange name is required"})
        
        if not regionid or not regionid.isdigit():
            return jsonify({"status": "error", "message": "Valid region is required"})
        
        # Check if exchange already exists
        existing = fetch_one("SELECT exchangeid FROM exchange WHERE exchangename = %s", (exchangename,))
        if existing:
            return jsonify({"status": "error", "message": "Exchange already exists"})
        
        # Create the exchange
        execute_change_query("INSERT INTO exchange (exchangename, region) VALUES (%s, %s)", (exchangename, regionid))
        
        # Get the new exchange ID
        new_exchange = fetch_one("SELECT exchangeid FROM exchange WHERE exchangename = %s", (exchangename,), dictionary=True)
        
        return jsonify({
            "status": "success", 
            "exchange_id": new_exchange["exchangeid"],
            "exchange_name": exchangename
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@admin_bp.route('/complete_security_creation', methods=['POST'])
@admin_required
def complete_security_creation():
    try:
        # Get the pending bond data from session
        pending_bond = session.get('pending_bond')
        if not pending_bond:
            return jsonify({"status": "error", "message": "No pending security data found"})
        
        # Get the form data
        bondname = pending_bond['bondname']
        bondsymbol = pending_bond['bondsymbol']
        bondcategoryid = pending_bond['bondcategoryid']
        bondcurrencyid = request.form.get('bondcurrencyid', '').strip()
        bondexchangeid = request.form.get('bondexchangeid', '').strip()
        bondcountry = pending_bond['bondcountry']
        bondwebsite = pending_bond['bondwebsite']
        bondindustry = pending_bond['bondindustry']
        bondsector = pending_bond['bondsector']
        bonddescription = pending_bond['bonddescription']
        
        # Get sector ID
        sector_data = fetch_one("SELECT sectorid FROM sector WHERE sectorname = %s", (bondsector,), dictionary=True)
        if not sector_data:
            return jsonify({"status": "error", "message": "Invalid sector"})
        bondsectorid = sector_data["sectorid"]
        
        # Create the bond
        query = """INSERT INTO bond (bondname, bondsymbol, bondcategoryid, bondcurrencyid, bondcountry, bondexchangeid, bondwebsite, bondindustry, bondsectorid, bonddescription) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        execute_change_query(query, (bondname, bondsymbol, bondcategoryid, bondcurrencyid, bondcountry, bondexchangeid, bondwebsite, bondindustry, bondsectorid, bonddescription))
        
        # Clear the session
        session.pop('pending_bond', None)
        
        return jsonify({"status": "success", "message": f"Security {bondsymbol} successfully created"})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})