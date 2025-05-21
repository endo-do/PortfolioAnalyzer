"""Handles Twelve Data API requests"""


from config import TWELVE_DATA_KEY
import requests


def get_exchange_rate(symbol, date=None):
    url = "https://api.twelvedata.com/exchange_rate"
    params = {
        "symbol": symbol,
        "apikey": TWELVE_DATA_KEY
    }
    if date:
        params["date"] = date  # format: "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"

    response = requests.get(url, params=params)
    return response.json()
