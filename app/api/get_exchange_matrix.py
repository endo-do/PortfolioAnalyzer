"""Fetch exchange rates for multiple currency pairs using yfinance."""

import yfinance as yf
from itertools import permutations
import warnings
import logging
from config import YAHOO_FINANCE_EXCHANGE_PERIOD_DAYS

# Suppress yfinance warnings and HTTP errors
warnings.filterwarnings('ignore')
logging.getLogger('yfinance').setLevel(logging.ERROR)


def get_exchange_matrix(currencies: list) -> dict:
    """
    Fetch today's exchange rates for all permutations of the given currencies.
    
    Args:
        currencies (list of str): Currency codes, e.g., ['USD', 'CHF', 'EUR']

    Returns:
        dict: Mapping like {'USDCHF': 0.89, 'CHFUSD': 1.12, 'EURUSD': 1.09, ...}
              If data is unavailable, value is None. Each currency maps to itself as 1.0 (e.g., 'USDUSD': 1.0)
    """
    if not currencies or not isinstance(currencies, list):
        return {}

    pairs = list(permutations(currencies, 2))  # e.g., [('USD', 'CHF'), ('CHF', 'USD'), ...]
    symbols = [f"{a}{b}=X" for a, b in pairs]

    try:
        # Suppress HTTP errors and warnings during download
        import sys
        from contextlib import redirect_stderr
        from io import StringIO
        
        # Redirect stderr to suppress HTTP 404 errors
        with redirect_stderr(StringIO()):
            # Download configured period of data for all currency pairs
            data = yf.download(
                symbols,
                period=f"{YAHOO_FINANCE_EXCHANGE_PERIOD_DAYS}d",
                group_by='ticker',
                threads=True,
                progress=False,
                auto_adjust=False
            )
    except Exception:
        # If download fails completely, return dict with all None (except self-mappings)
        exchange_rates = {f"{a}{b}": None for a, b in pairs}
        for c in currencies:
            exchange_rates[f"{c}{c}"] = 1.0
        return exchange_rates

    exchange_rates = {}

    for (a, b), symbol in zip(pairs, symbols):
        try:
            rate = data[symbol]["Close"].dropna().iloc[-1]
            exchange_rates[f"{a}{b}"] = float(rate) if rate is not None else None
        except (KeyError, IndexError, TypeError):
            exchange_rates[f"{a}{b}"] = None  # If data is missing or invalid

    # Add identity rates (e.g., USDUSD = 1.0)
    for c in currencies:
        exchange_rates[f"{c}{c}"] = 1.0

    return exchange_rates