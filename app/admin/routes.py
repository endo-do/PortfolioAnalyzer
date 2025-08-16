"""Admin routes for managing securities, currencies, and users."""

from datetime import date
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_required
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

@admin_bp.route('/')
@login_required
def admin_dashboard():
    admin_required()
    return render_template('admin_dashboard.html')

@admin_bp.route('/securityoverview')
@login_required
def securityoverview():
    admin_required()
    bonds = get_all_bonds()
    for bond in bonds:
        if bond['bondrate'] == 'N/A':
            bond['bondrate'] = None
        else:
            try:
                bond['bondrate'] = float(bond['bondrate'])
            except ValueError:
                bond['bondrate'] = None
    currencies = get_all_currencies()
    categories = get_all_categories()
    return render_template('securityoverview.html', bonds=bonds, currencies=currencies, categories=categories)

@admin_bp.route('/securityview_admin/<int:bond_id>')
@login_required
def securityview_admin(bond_id):
    bond = get_full_bond(bond_id)
    currencies = get_all_currencies()
    categories = get_all_categories()
    return render_template('securityview_admin.html', bond=bond, currencies=currencies, categories=categories)

@admin_bp.route('/create_security', methods=['POST'])
@login_required
def create_security():
    admin_required()
    bondname = request.form.get('name')
    bondsymbol = request.form.get('bondsymbol')
    bondcategoryid = request.form.get('bondcategoryid')
    bondcurrencyid = request.form.get('bondcurrencyid')
    bondcountry = request.form.get('bondcountry')
    bondwebsite = request.form.get('bondwebsite')
    bondindustry = request.form.get('bondindustry')
    bondsector = request.form.get('bondsector')
    bonddescription = request.form.get('bonddescription')
    bondrate, trade_date = get_eod(bondsymbol)

    existing_bond = fetch_one("""SELECT bondid FROM bond WHERE bondsymbol = %s""", (bondsymbol,))
    
    if existing_bond:
        flash(f"Security {bondsymbol} does is exist already", 'warning')
        return redirect(url_for('admin.securityoverview'))
    else:
        query = """INSERT INTO bond (bondname, bondsymbol, bondcategoryid, bondcurrencyid, bondcountry, bondwebsite, bondindustry, bondsector, bonddescription) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        execute_change_query(query, (bondname, bondsymbol, bondcategoryid, bondcurrencyid, bondcountry, bondwebsite, bondindustry, bondsector, bonddescription))
        flash(f"Security {bondsymbol} successfully created", 'success')

    bondid = fetch_one("""SELECT bondid FROM bond WHERE bondsymbol = %s""", (bondsymbol,), dictionary=True)['bondid']
    existing_data = fetch_one("""SELECT bondid FROM bonddata WHERE bondid = %s AND bonddatalogtime = %s""", (bondid, trade_date))

    if not existing_data:
        query = """INSERT INTO bonddata (bondid, bonddatalogtime, bondrate) VALUES (%s, %s, %s)"""
        execute_change_query(query, (bondid, trade_date, bondrate))

    execute_change_query("""
        UPDATE status SET securities = %s WHERE id = 1""",
        (date.today(),))
    
    return redirect(url_for('admin.securityoverview'))

@admin_bp.route('/edit_security/<int:bondid>', methods=['POST'])
@login_required
def edit_security(bondid):
    admin_required()

    name = request.form['name']
    symbol = request.form['bondsymbol']
    categoryid = request.form['bondcategoryid']
    currencyid = request.form['bondcurrencyid']
    country = request.form.get('bondcountry')
    website = request.form.get('bondwebsite')
    industry = request.form.get('bondindustry')
    sector = request.form.get('bondsector')
    description = request.form['bonddescription']

    execute_change_query("""
            UPDATE bond SET
              bondname = %s,
              bondsymbol = %s,
              bondcategoryid = %s,
              bondcurrencyid = %s,
              bondcountry = %s,
              bondwebsite = %s,
              bondindustry = %s,
              bondsector = %s,
              bonddescription = %s
            WHERE bondid = %s
        """, (name, symbol, categoryid, currencyid, country, website, industry, sector, description, bondid))
    
    flash(f"Security {symbol} successfully updated", "success")

    return redirect(url_for('admin.securityview_admin', bond_id=bondid))

@admin_bp.route('/delete_security/<int:bondid>', methods=['POST'])
@login_required
def delete_security(bondid):
    admin_required()
    bondsymbol = fetch_one("SELECT bondsymbol FROM bond WHERE bondid = %s", (bondid,), dictionary=True)['bondsymbol']
    execute_change_query("""DELETE FROM bond WHERE bondid = %s""", (bondid,))
    flash(f"Security {bondsymbol} successfully deleted", 'success')
    return redirect(url_for('admin.securityoverview'))

@admin_bp.route('/currencyoverview')
@login_required
def currencyoverview():
    admin_required()
    currencies = get_all_currencies()
    return render_template('currencyoverview.html', currencies=currencies)

@admin_bp.route('/create_currency', methods=['POST'])
@login_required
def create_currency():
    admin_required()

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
@login_required
def delete_currency(currencyid):
    admin_required()
    currencycode = fetch_one("""SELECT currencycode FROM currency WHERE currencyid = %s""", (currencyid,), dictionary=True)['currencycode']
    try:
        execute_change_query("""DELETE FROM currency WHERE currencyid = %s""", (currencyid,))
        flash(f"Currency {currencycode} has been successfully deleted", "success")
    except mysql.connector.errors.IntegrityError as e:
        flash(f"Cannot delete Currency {currencycode} because its referenced in other records.", "danger")
    return redirect(url_for('admin.currencyoverview'))


@admin_bp.route('/useroverview')
@login_required
def useroverview():
    admin_required()
    users = get_all_users()
    return render_template('useroverview.html', users=users)


@admin_bp.route('/delete_user/<int:userid>', methods=['POST'])
@login_required
def delete_user(userid):
    admin_required()
    if userid == 1:
        flash('Cannot delete the admin user.', 'danger')
        return redirect(url_for('admin.useroverview'))
    username = fetch_one("""SELECT username FROM user where userid = %s""", (userid,), dictionary=True)['username']
    execute_change_query("""DELETE FROM user WHERE userid = %s""", (userid,))
    flash(f"User {username} has been successfully deleted", "success")
    return redirect(url_for('admin.useroverview'))


@admin_bp.route('/edit_user/<int:userid>', methods=['POST'])
@login_required
def edit_user(userid):
    admin_required()

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
@login_required
def create_user():
    admin_required()

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