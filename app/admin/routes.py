from flask import render_template, abort, url_for, redirect
from flask_login import current_user, login_required
from . import admin_bp
from app.database.tables.bond.get_all_bonds import get_all_bonds
from app.database.tables.bond.get_full_bond import get_full_bond
from app.database.helpers.fetch_all import fetch_all

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
    query = """SELECT currencyid as id, currencycode FROM currency"""
    currencies = fetch_all(query=query, dictionary=True)
    query = """SELECT bondcategoryid as id, bondcategoryname FROM bondcategory"""
    categories = fetch_all(query=query, dictionary=True)
    return render_template('securityoverview.html', bonds=bonds, currencies=currencies, categories=categories)

@admin_bp.route('/securityview/<int:bond_id>')
@login_required
def securityview(bond_id):
    bond = get_full_bond(bond_id)
    return render_template('securityview.html', bond=bond, backurl = url_for('admin.securityoverview'))

@admin_bp.route('/create_security', methods=['POST'])
@login_required
def create_security():
    if not current_user.is_admin:
        abort(403)
    # Logic to create a new security would go here
    # This is a placeholder for the actual implementation
    return redirect(url_for('admin.securityoverview'))