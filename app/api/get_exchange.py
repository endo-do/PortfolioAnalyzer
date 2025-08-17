import yfinance as yf

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
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return info.get('exchange') or "Unknown"
    except Exception:
        return "Unknown"