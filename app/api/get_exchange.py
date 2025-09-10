import yfinance as yf
import warnings
import logging
from contextlib import redirect_stderr
from io import StringIO

# Suppress yfinance warnings and logs
warnings.filterwarnings('ignore')
logging.getLogger('yfinance').setLevel(logging.ERROR)

def get_exchange(symbol):
    """
    Returns the exchange for a given security symbol using yfinance.
    
    Args:
        symbol (str): The ticker symbol of the security.
    
    Returns:
        str: The exchange name, or "Unknown" if unavailable.
    """
    if not symbol or not isinstance(symbol, str):
        return "Unknown"

    try:
        # Suppress HTTP errors and warnings during download
        with redirect_stderr(StringIO()):
            ticker = yf.Ticker(symbol)
            info = ticker.info
        return info.get('exchange') or "Unknown"
    except Exception:
        return "Unknown"