"""Fetch end-of-day price and date for stock symbol using yfinance."""

import yfinance as yf
import warnings
import logging
from contextlib import redirect_stderr
from io import StringIO

# Suppress yfinance warnings and logs
warnings.filterwarnings('ignore')
logging.getLogger('yfinance').setLevel(logging.ERROR)

def get_eod(symbol):
    """
    Fetches the end-of-day closing price, volume, and trading date for a given security symbol using yfinance.

    Args:
        symbol (str): The ticker symbol of the security.

    Returns:
        tuple: (closing price as float, volume as int, trading date as 'YYYY-MM-DD'),
               or (None, None, None) if not available or on error.
    """
    if not symbol or not isinstance(symbol, str):
        return None, None, None

    try:
        # Suppress HTTP errors and warnings during download
        with redirect_stderr(StringIO()):
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d")  # Fetch last few days to cover weekends/holidays

        if hist.empty or "Close" not in hist.columns:
            return None, None, None

        last_valid_row = hist.dropna().iloc[-1]
        latest_close = last_valid_row["Close"]
        latest_volume = last_valid_row["Volume"]
        trade_date = last_valid_row.name.strftime("%Y-%m-%d")  # index holds the date

        return (
            float(latest_close) if latest_close is not None else None,
            int(latest_volume) if latest_volume is not None else None,
            trade_date
        ) if latest_close is not None else (None, None, None)

    except Exception:
        return None, None, None
