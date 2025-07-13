from flask import render_template, abort
from flask_login import current_user, login_required
from . import admin_bp
from app.database.tables.bond.get_all_bonds import get_all_bonds

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
    return render_template('securityoverview.html', bonds=bonds)