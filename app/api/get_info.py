"""Fetch financial information for a given security symbol using yfinance."""

import yfinance as yf
import re


def get_info(symbol):
    """
    Fetches financial information for a given security symbol using yfinance.

    Args:
        symbol (str): The ticker symbol of the security.

    Returns:
        dict: A dictionary containing the financial information of the security.
              Returns an empty dictionary if data is unavailable or an error occurs.
    """
    if not symbol or not isinstance(symbol, str):
        return {}

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        if not info or not isinstance(info, dict):
            return {}

        name = info.get('longName', 'N/A')
        country = info.get('country', 'N/A')
        currency = info.get('currency', 'N/A')
        website = info.get('website', 'N/A')
        industry = info.get('industry', 'N/A')
        sector = info.get('sector', 'N/A')
        exchange = info.get('exchange', 'N/A')

        # --- Extract the first sentence from the business summary ---
        long_description = info.get('longBusinessSummary', 'N/A')
        description = "N/A"
        if isinstance(long_description, str) and long_description.strip():
            match = re.match(r'^(.*?[.!?])(?=\s+[A-Z]|$)', long_description, re.DOTALL)
            description = match.group(1).strip() if match else long_description.strip()

        # --- Category mapping ---
        category = None
        quote_type = info.get('quoteType', '').upper()
        type_disp = info.get('typeDisp', '').capitalize()

        if quote_type == "EQUITY" or type_disp == "Equity":
            category = "Share"
        elif quote_type == "ETF" or type_disp == "Etf":
            category = "ETF"
        elif quote_type == "MUTUALFUND" or type_disp == "Fund":
            category = "Managed Fund"

        return {
            "symbol": symbol,
            "name": name,
            "country": country,
            "exchange": exchange,
            "currency": currency,
            "website": website,
            "industry": industry,
            "sector": sector,
            "description": description,
            "category": category
        }

    except (KeyError, TypeError, ValueError, IndexError):
        return {}
