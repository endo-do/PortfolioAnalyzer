from app.database.helpers.fetch_one import fetch_one

def get_currency_code_by_id(currency_id):
    result = fetch_one('SELECT currencycode FROM currency WHERE currencyid = %s', (currency_id,))
    return result[0] if result else None