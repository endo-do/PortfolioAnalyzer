from app.database.helpers.fetch_all import fetch_all

def get_all_currency_pairs():
    currencies = [row[0] for row in fetch_all('SELECT currencyid FROM currency')]
    pairs = [(base, quote) for base in currencies for quote in currencies]
    return pairs