"""Handles Twelve Data API requests"""


from config import TWELVE_DATA_KEY
import requests


def get_exchange_rate(symbol, date=None):
    """
    Fetch the current exchange rate of the currencies

    Args:
        symbol (CODE1/CODE2): The conversion of the currencies as a symbol
        date (date, optional): Date of conversion rate. Defaults to None.

    Returns:
        _type_: _description_
    """
    
    url = "https://api.twelvedata.com/exchange_rate"
    params = {
        "symbol": symbol,
        "apikey": TWELVE_DATA_KEY
    }
    if date:
        params["date"] = date  # format: "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"

    response = requests.get(url, params=params)
    return response.json()

def get_eod_price(symbol, date=None):
    """
    Fetch end-of-day price for a given symbol from Twelve Data API

    Args:
        symbol (str): Ticker symbol of the instrument
        date (str, optional): Date in 'YYYY-MM-DD' format. If None, fetches latest EOD price

    Returns:
        dict: JSON response from the API including 'close' price if successful.
    """
    url = "https://api.twelvedata.com/eod"
    params = {
        "symbol": symbol,
        "apikey": TWELVE_DATA_KEY
    }
    if date:
        params["date"] = date

    response = requests.get(url, params=params)
    return response.json()