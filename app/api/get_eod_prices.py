"""Fetch end-of-day prices for stock symbols using yfinance."""

import yfinance as yf
import pandas as pd


def get_eod_prices(symbols):
    """
    Fetches the latest end-of-day closing prices for a list of symbols using yfinance.

    Args:
        symbols (list of str): List of ticker symbols, e.g. ['AAPL', 'MSFT']

    Returns:
        dict: Mapping of symbol to closing price (float). If no data or error, value is None.
    """
    prices = {}

    if not symbols or not isinstance(symbols, list):
        return prices  # Return empty dict if symbols is not a valid list

    try:
        # Download last 1 day of data for all symbols
        data = yf.download(
            symbols,
            period="1d",
            group_by='ticker',
            threads=True,
            progress=False,
            auto_adjust=True
        )
    except Exception as e:
        for symbol in symbols:
            prices[symbol] = None
        return prices

    # Multiple symbols: multi-index DataFrame
    if isinstance(data.columns, pd.MultiIndex):
        for symbol in symbols:
            try:
                close_price = data[symbol]['Close'].iloc[-1]
                prices[symbol] = float(close_price) if not pd.isna(close_price) else None
            except (KeyError, IndexError, TypeError):
                prices[symbol] = None
    else:
        # Single symbol case
        try:
            close_price = data['Close'].iloc[-1]
            prices[symbols[0]] = float(close_price) if not pd.isna(close_price) else None
        except (KeyError, IndexError, TypeError):
            prices[symbols[0]] = None

    return prices