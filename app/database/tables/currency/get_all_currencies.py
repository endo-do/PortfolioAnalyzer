from app.database.helpers.fetch_all import fetch_all


def get_all_currencies():
    query = """SELECT currencyid, currencycode, currencyname FROM currency ORDER BY currencycode"""
    currencies = fetch_all(query=query, dictionary=True)
    return currencies