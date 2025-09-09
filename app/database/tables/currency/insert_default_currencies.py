from app.database.helpers.fetch_one import fetch_one
from app.database.helpers.execute_change_query import execute_change_query
from app.database.tables.exchangerate.fetch_daily_exchangerates import fetch_daily_exchangerates

def insert_default_currencies():
    currencies = [
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
        ("CHF", "Swiss Franc"),
        ("GBP", "British Pound"),
        ("JPY", "Japanese Yen"),
        ("CNY", "Chinese Yuan"),
        ("CAD", "Canadian Dollar"),
        ("AUD", "Australian Dollar")
    ]

    for code, name in currencies:
        query = "INSERT INTO currency (currencycode, currencyname) VALUES (%s, %s)"
        execute_change_query(query, (code, name))

    fetch_daily_exchangerates()
    print(f"    ✅ Default currencies inserted successfully")