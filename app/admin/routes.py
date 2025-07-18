from flask import render_template, abort, url_for, redirect, request, flash
from flask_login import current_user, login_required
from . import admin_bp
from app.database.tables.bond.get_all_bonds import get_all_bonds
from app.database.tables.bond.get_full_bond import get_full_bond
from app.database.helpers.fetch_all import fetch_all
from app.database.helpers.fetch_one import fetch_one
from app.database.helpers.execute_change_query import execute_change_query
from app.database.tables.exchangerate.fetch_daily_exchangerates import fetch_daily_exchangerates
from app.api.get_eod import get_eod
from datetime import date
from werkzeug.security import generate_password_hash

@admin_bp.route('/')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    return render_template('admin_dashboard.html')

@admin_bp.route('/securityoverview')
@login_required
def securityoverview():
    if not current_user.is_admin:
        abort(403)
    bonds = get_all_bonds()
    for bond in bonds:
        if bond['bondrate'] == 'N/A':
            bond['bondrate'] = None
        else:
            try:
                bond['bondrate'] = float(bond['bondrate'])
            except ValueError:
                bond['bondrate'] = None
    query = """SELECT currencyid, currencycode FROM currency"""
    currencies = fetch_all(query=query, dictionary=True)
    query = """SELECT bondcategoryid, bondcategoryname FROM bondcategory"""
    categories = fetch_all(query=query, dictionary=True)
    return render_template('securityoverview.html', bonds=bonds, currencies=currencies, categories=categories)

@admin_bp.route('/securityview/<int:bond_id>')
@login_required
def securityview(bond_id):
    bond = get_full_bond(bond_id)
    query = """SELECT currencyid, currencycode FROM currency"""
    currencies = fetch_all(query=query, dictionary=True)
    query = """SELECT bondcategoryid, bondcategoryname FROM bondcategory"""
    categories = fetch_all(query=query, dictionary=True)
    return render_template('securityview.html', bond=bond, backurl = url_for('admin.securityoverview'), currencies=currencies, categories=categories)

@admin_bp.route('/create_security', methods=['POST'])
@login_required
def create_security():
    if not current_user.is_admin:
        abort(403)
    bondname = request.form.get('name')
    bondsymbol = request.form.get('bondsymbol')
    bondcategoryid = request.form.get('bondcategoryid')
    bondcurrencyid = request.form.get('bondcurrencyid')
    bondcountry = request.form.get('bondcountry')
    bondwebsite = request.form.get('bondwebsite')
    bondindustry = request.form.get('bondindustry')
    bondsector = request.form.get('bondsector')
    bonddescription = request.form.get('bonddescription')

    bondrate = get_eod(bondsymbol)

    existing_bond = fetch_one("""SELECT bondid FROM bond WHERE bondsymbol = %s""", (bondsymbol,))
    
    if existing_bond:
        query = """UPDATE bond SET bondname = %s, bondcategoryid = %s, bondcurrencyid = %s, bondcountry = %s, bondwebsite = %s, bondindustry = %s, bondsector = %s, bonddescription = %s WHERE bondsymbol = %s"""
        execute_change_query(query, (bondname, bondcategoryid, bondcurrencyid, bondcountry, bondwebsite, bondindustry, bondsector, bonddescription, bondsymbol))
    else:
        query = """INSERT INTO bond (bondname, bondsymbol, bondcategoryid, bondcurrencyid, bondcountry, bondwebsite, bondindustry, bondsector, bonddescription) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        execute_change_query(query, (bondname, bondsymbol, bondcategoryid, bondcurrencyid, bondcountry, bondwebsite, bondindustry, bondsector, bonddescription))
    
    bondid = fetch_one("""SELECT bondid FROM bond WHERE bondsymbol = %s""", (bondsymbol,), dictionary=True)['bondid']
    existing_data = fetch_one("""SELECT bondid FROM bonddata WHERE bondid = %s AND bonddatalogtime = %s""", (bondid, date.today()))

    if not existing_data:
        query = """INSERT INTO bonddata (bondid, bonddatalogtime, bondrate) VALUES (%s, %s, %s)"""
        execute_change_query(query, (bondid, date.today(), bondrate))

    execute_change_query("""
        UPDATE status SET securities = %s WHERE id = 1""",
        (date.today(),))
    
    return redirect(url_for('admin.securityoverview'))

@admin_bp.route('/edit_security/<int:bondid>', methods=['POST'])
@login_required
def edit_security(bondid):
    if not current_user.is_admin:
        abort(403)

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

    eod = get_eod(symbol)  # Update bond rate from EOD data
    execute_change_query("""
        UPDATE bonddata SET
          bondrate = %s
        WHERE bondid = %s AND bonddatalogtime = %s
    """, (eod, bondid, date.today()))
    
    execute_change_query("""
        UPDATE status SET securities = %s WHERE id = 1""",
        (date.today(),))

    return redirect(url_for('admin.securityview', bond_id=bondid))

@admin_bp.route('/delete_security/<int:bondid>', methods=['POST'])
@login_required
def delete_security(bondid):
    if not current_user.is_admin:
        abort(403)
    execute_change_query("""DELETE FROM bond WHERE bondid = %s""", (bondid,))
    return redirect(url_for('admin.securityoverview'))

@admin_bp.route('/currencyoverview')
@login_required
def currencyoverview():
    if not current_user.is_admin:
        abort(403)
    query = """SELECT currencyid, currencycode, currencyname FROM currency"""
    currencies = fetch_all(query=query, dictionary=True)
    return render_template('currencyoverview.html', currencies=currencies)

@admin_bp.route('/create_currency', methods=['POST'])
@login_required
def create_currency():
    if not current_user.is_admin:
        abort(403)

    currencycode = request.form.get('currencycode')
    currencyname = request.form.get('currencyname')

    existing_currency = fetch_one("""SELECT currencyid FROM currency WHERE currencycode = %s""", (currencycode,))
    if existing_currency:
        query = """UPDATE currency SET currencyname = %s WHERE currencycode = %s"""
        execute_change_query(query, (currencyname, currencycode))
    else:
        query = """INSERT INTO currency (currencycode, currencyname) VALUES (%s, %s)"""
        execute_change_query(query, (currencycode, currencyname))
    
    fetch_daily_exchangerates()  # Update exchange rates after adding a new currency

    return redirect(url_for('admin.currencyoverview'))

@admin_bp.route('/edit_currency/<int:currencyid>', methods=['POST'])
@login_required
def edit_currency():
    if not current_user.is_admin:
        abort(403)

@admin_bp.route('/delete_currency/<int:currencyid>', methods=['POST'])
@login_required
def delete_currency(currencyid):
    if not current_user.is_admin:
        abort(403)
    execute_change_query("""DELETE FROM currency WHERE currencyid = %s""", (currencyid,))
    return redirect(url_for('admin.currencyoverview'))


@admin_bp.route('/useroverview')
@login_required
def useroverview():
    if not current_user.is_admin:
        abort(403)
    query = """SELECT userid, username, is_admin FROM user"""
    users = fetch_all(query=query, dictionary=True)
    return render_template('useroverview.html', users=users)


@admin_bp.route('/delete_user/<int:userid>', methods=['POST'])
@login_required
def delete_user(userid):
    if not current_user.is_admin:
        abort(403)
    if userid == 1:
        flash('Cannot delete the admin user.', 'danger')
        return redirect(url_for('admin.useroverview'))
    execute_change_query("""DELETE FROM user WHERE userid = %s""", (userid,))
    return redirect(url_for('admin.useroverview'))


@admin_bp.route('/edit_user/<int:userid>', methods=['POST'])
@login_required
def edit_user(userid):
    if not current_user.is_admin:
        abort(403)

    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin')

    if userid == 1:
        flash('Cannot edit the admin user.', 'danger')
        return redirect(url_for('admin.useroverview'))

    if password:
        password = generate_password_hash(password)
    else:
        # If no password is provided, keep the existing one
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

    return redirect(url_for('admin.useroverview'))

@admin_bp.route('/create_user', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        abort(403)

    username = request.form.get('username')
    password = request.form.get('password')
    password_confirm = request.form.get('passwordconfirm')
    is_admin = request.form.get('is_admin')

    # alredy exists check

    if password != password_confirm:
        flash('Passwords do not match.', 'danger')
        return redirect(url_for('admin.useroverview'))
    
    password_hashed = generate_password_hash(password)
    is_admin_bool = True if is_admin == 'on' else False

    execute_change_query("""
        INSERT INTO user (username, userpwd, is_admin)
        VALUES (%s, %s, %s)
    """, (username, password_hashed, is_admin_bool))

    flash('User created successfully.', 'success')
    return redirect(url_for('admin.useroverview'))