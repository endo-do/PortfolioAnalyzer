"""Fetch end-of-day prices for stock symbols using yfinance."""

import yfinance as yf
import pandas as pd


import yfinance as yf
import pandas as pd

def get_eod_prices(symbols):
    """
    Fetches the latest end-of-day closing prices and trading dates for a list of symbols using yfinance.

    Args:
        symbols (list of str): List of ticker symbols, e.g. ['AAPL', 'MSFT']

    Returns:
        dict: Mapping of symbol -> (closing price (float), trading date 'YYYY-MM-DD').
              If no data or error, value is (None, None).
    """
    results = {}

    if not symbols or not isinstance(symbols, list):
        return results  # Return empty dict if symbols is not a valid list

    try:
        # Download last 5 days to cover weekends/holidays
        data = yf.download(
            symbols,
            period="5d",
            group_by="ticker",
            threads=True,
            progress=False,
            auto_adjust=True
        )
    except Exception:
        for symbol in symbols:
            results[symbol] = (None, None)
        return results

    # Multiple symbols: multi-index DataFrame
    if isinstance(data.columns, pd.MultiIndex):
        for symbol in symbols:
            try:
                sub = data[symbol].dropna()
                last_valid_idx = sub.index[-1]
                close_price = sub.loc[last_valid_idx, "Close"]
                results[symbol] = (
                    float(close_price) if not pd.isna(close_price) else None,
                    last_valid_idx.strftime("%Y-%m-%d")
                )
            except Exception:
                results[symbol] = (None, None)
    else:
        # Single symbol case
        try:
            sub = data.dropna()
            last_valid_idx = sub.index[-1]
            close_price = sub.loc[last_valid_idx, "Close"]
            results[symbols[0]] = (
                float(close_price) if not pd.isna(close_price) else None,
                last_valid_idx.strftime("%Y-%m-%d")
            )
        except Exception:
            results[symbols[0]] = (None, None)

    return results