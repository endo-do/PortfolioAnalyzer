from flask import render_template, abort, request
from flask_login import login_required, current_user
from . import admin_bp
from app.database.bond_data import get_bonds

@admin_bp.route('/')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    return render_template('admin_dashboard.html')

@admin_bp.route('/bonds')
@login_required
def admin_bonds():
    if not current_user.is_admin:
        abort(403)

    bonds = get_bonds()
    return render_template('bonds.html', bonds=bonds)