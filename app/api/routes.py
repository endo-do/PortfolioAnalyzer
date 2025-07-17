from . import api_bp
from app.api.get_info import get_info
from flask_login import current_user, login_required
from flask import jsonify

@api_bp.route('/securityinfo/<string:symbol>')
@login_required
def securityinfo(symbol):
    info = get_info(symbol)
    if info:
        return jsonify(info)
    else:
        return jsonify({"error": "Info not found"}), 404