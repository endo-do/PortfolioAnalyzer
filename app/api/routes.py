"""API routes"""

from . import api_bp
from app.api.get_info import get_info
from flask_login import current_user, login_required
from flask import jsonify
from app.api.get_eod import get_eod

@api_bp.route('/securityinfo/<string:symbol>')
@login_required
def securityinfo(symbol):
    info = get_info(symbol)
    if info:
        return jsonify(info)
    else:
        return jsonify({"error": "Info not found"}), 404
    
@api_bp.route('/get_price/<string:symbol>')
@login_required
def get_price(symbol):
    price = get_eod(symbol)
    if price is None:
        return {"error": "Price not found"}, 404
    return {"symbol": symbol, "price": price}
