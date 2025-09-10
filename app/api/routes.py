"""API routes"""

from . import api_bp
from app.api.get_info import get_info
from app.api.get_eod import get_eod
from app.api.get_exchange import get_exchange
from app.api.get_exchange_matrix import get_exchange_matrix
from app.api.get_last_trading_day import get_last_trading_day
from flask_login import current_user, login_required
from flask import jsonify, request
import yfinance as yf

@api_bp.route('/securityinfo/<string:symbol>')
def securityinfo(symbol):
    info = get_info(symbol)
    if info:
        return jsonify(info)
    else:
        return jsonify({"error": "Info not found"}), 404
    
@api_bp.route('/get_price/<string:symbol>')
def get_price(symbol):
    price, volume, trade_date = get_eod(symbol)
    if price is None:
        return {"error": "Price not found"}, 404
    return {"symbol": symbol, "price": price, "volume": volume, "trade_date": trade_date}

@api_bp.route('/exchange_rates')
def exchange_rates():
    """Get exchange rates for currency pairs."""
    from_currency = request.args.get('from', 'USD')
    to_currency = request.args.get('to', 'EUR')
    
    try:
        # Create a simple exchange rate lookup
        symbol = f"{from_currency}{to_currency}=X"
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        
        if hist.empty:
            return jsonify({"error": "Exchange rate not found"}), 404
            
        rate = hist['Close'].iloc[-1]
        return jsonify({f"{from_currency}_{to_currency}": float(rate)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/security_info/<string:symbol>')
def security_info(symbol):
    """Get security information."""
    info = get_info(symbol)
    if info:
        return jsonify(info)
    else:
        return jsonify({"error": "Security info not found"}), 404

@api_bp.route('/last_trading_day')
def last_trading_day():
    """Get last trading day."""
    try:
        last_day = get_last_trading_day()
        return jsonify({"last_trading_day": last_day})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/exchange_matrix')
def exchange_matrix():
    """Get exchange rate matrix."""
    currencies = request.args.getlist('currencies')
    if not currencies:
        currencies = ['USD', 'EUR', 'CHF']
    
    try:
        matrix = get_exchange_matrix(currencies)
        return jsonify(matrix)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/eod_prices/<string:symbol>')
def eod_prices(symbol):
    """Get end-of-day prices."""
    try:
        price, volume, trade_date = get_eod(symbol)
        if price is None:
            return jsonify({"error": "Price not found"}), 404
        return jsonify({"symbol": symbol, "price": price, "volume": volume, "trade_date": trade_date})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
