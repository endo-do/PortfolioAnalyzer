"""Fetch end-of-day price for stock symbol using yfinance."""

import yfinance as yf


def get_eod(symbol):
    """
    Fetches the end-of-day closing price for a given security symbol using yfinance.

    Args:
        symbol (str): The ticker symbol of the security.

    Returns:
        float: Latest closing price of the security, or None if not available or on error.
    """
    if not symbol or not isinstance(symbol, str):
        return None

    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d")  # Fetch last 2 days to avoid empty close

        if hist.empty or 'Close' not in hist.columns:
            return None

        latest_close = hist['Close'].iloc[-1]
        return float(latest_close) if latest_close is not None else None

    except (IndexError, ValueError, KeyError, TypeError):
        return None
