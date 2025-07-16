from app.database.helpers.fetch_one import fetch_one

def get_currency_id_by_code(currency_code):
    result = fetch_one('SELECT currencyid FROM currency WHERE currencycode = %s', (currency_code,))
    return result[0] if result else None