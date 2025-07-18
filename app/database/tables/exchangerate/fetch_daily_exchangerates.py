from datetime import date
from app.database.tables.exchangerate.exchange_rate_exists import exchange_rate_exists
from app.database.helpers.execute_change_query import execute_change_query
from app.database.tables.currency.get_currency_id_by_code import get_currency_id_by_code
from app.database.helpers.fetch_all import fetch_all
from app.database.helpers.fetch_one import fetch_one
from app.api.get_exchange_matrix import get_exchange_matrix

def fetch_daily_exchangerates():
    """
    Fetches todays exchange rates for all currencies in the database
    and inserts them into the exchangerate table if they do not already exist.
    """

    # Check last full update
    last_update = fetch_one("SELECT exchangerates FROM status WHERE id = 1")[0]

    if last_update == date.today():
        print("Exchangerates already updated today, skipping.")
        return

    print("Fetching today's exchange rates...")

    # Fetch all currencies
    all_currencies = [row[0] for row in fetch_all("SELECT currencycode FROM currency")]

    # Get full exchange matrix for all currencies
    exchange_rates = get_exchange_matrix(all_currencies)

    # Insert or update all exchange rates
    for pair, rate in exchange_rates.items():
        from_currency, to_currency = pair[:3], pair[3:]
        from_id = get_currency_id_by_code(from_currency)
        to_id = get_currency_id_by_code(to_currency)

        if not from_id or not to_id or not rate:
            continue

        # Upsert logic (pseudo):
        if exchange_rate_exists(from_id, to_id, log_date=date.today()):
            execute_change_query("""
                UPDATE exchangerate
                SET exchangerate = %s
                WHERE fromcurrencyid = %s AND tocurrencyid = %s AND exchangeratelogtime = %s
            """, (rate, from_id, to_id, date.today()))
        else:
            execute_change_query("""
                INSERT INTO exchangerate (fromcurrencyid, tocurrencyid, exchangerate, exchangeratelogtime)
                VALUES (%s, %s, %s, %s)
            """, (from_id, to_id, rate, date.today()))

    # Update global status
    execute_change_query("""
        UPDATE status SET exchangerates = %s WHERE id = 1""",
        (date.today(),))