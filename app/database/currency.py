from app.database.db import fetch_all, fetch_one

def get_all_currency_pairs():
    currencies = [row[0] for row in fetch_all('SELECT currencyid FROM currencies')]
    pairs = [(base, quote) for base in currencies for quote in currencies]
    return pairs

def get_currency_code_by_id(currency_id):
    result = fetch_one('SELECT currencycode FROM currencies WHERE currencyid = %s', (currency_id,))
    return result[0] if result else None