import yfinance as yf

def get_last_trading_day() -> str | None:
    """
    Returns the last trading day for the market in YYYY-MM-DD format.
    Uses a liquid market ETF as a proxy to handle weekends and holidays.
    
    Returns:
        str: Last trading day as 'YYYY-MM-DD', or None if no data.
    """
    try:
        # Use SPY as a liquid proxy for the overall market
        hist = yf.Ticker("SPY").history(period="7d")  # last 7 days to cover holidays/weekends
        
        if hist.empty or 'Close' not in hist.columns:
            return None
        
        last_valid = hist['Close'].last_valid_index()
        if last_valid is None:
            return None
        
        return last_valid.strftime("%Y-%m-%d")
    
    except Exception:
        return None