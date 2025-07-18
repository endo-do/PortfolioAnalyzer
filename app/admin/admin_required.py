from flask import abort
from flask_login import current_user

def admin_required():
    if not current_user.is_admin:
        abort(403)