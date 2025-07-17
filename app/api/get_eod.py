import yfinance as yf

def get_eod(symbol):
    """
    Fetches the eod for a given security symbol using yfinance.

    Args:
        symbol (str): The ticker symbol of the security.

    Returns:
        flot: Latest closing price of the security, or None if not available.
    """
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d")  # get last 2 days to ensure we get at least 1 close

        if hist.empty:
            return None
        
        # Take the last closing price available
        latest_close = hist['Close'].iloc[-1]
        return float(latest_close)

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None