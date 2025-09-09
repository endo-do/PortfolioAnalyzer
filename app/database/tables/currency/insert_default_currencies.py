from app.database.helpers.fetch_one import fetch_one
from app.database.helpers.execute_change_query import execute_change_query
from app.database.tables.exchangerate.fetch_daily_exchangerates import fetch_daily_exchangerates

def insert_default_currencies():
    currencies = [
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
        ("JPY", "Japanese Yen"),
        ("GBP", "British Pound"),
        ("AUD", "Australian Dollar"),
        ("CAD", "Canadian Dollar"),
        ("CHF", "Swiss Franc"),
        ("CNY", "Chinese Yuan"),
        ("HKD", "Hong Kong Dollar"),
        ("NZD", "New Zealand Dollar"),
        ("SEK", "Swedish Krona"),
        ("KRW", "South Korean Won"),
        ("SGD", "Singapore Dollar"),
        ("NOK", "Norwegian Krone"),
        ("MXN", "Mexican Peso"),
        ("INR", "Indian Rupee"),
        ("RUB", "Russian Ruble"),
        ("ZAR", "South African Rand"),
        ("TRY", "Turkish Lira"),
        ("BRL", "Brazilian Real"),
        ("TWD", "New Taiwan Dollar"),
        ("DKK", "Danish Krone"),
        ("PLN", "Polish Zloty"),
        ("THB", "Thai Baht"),
        ("IDR", "Indonesian Rupiah")
    ]


    for code, name in currencies:
        query = "INSERT INTO currency (currencycode, currencyname) VALUES (%s, %s)"
        execute_change_query(query, (code, name))

    fetch_daily_exchangerates()
    print(f"    ✅ Default currencies inserted successfully")