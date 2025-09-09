from datetime import date
from app.database.tables.exchangerate.exchange_rate_exists import exchange_rate_exists
from app.database.helpers.execute_change_query import execute_change_query
from app.database.tables.currency.get_currency_id_by_code import get_currency_id_by_code
from app.database.helpers.fetch_all import fetch_all
from app.database.helpers.fetch_one import fetch_one
from app.api.get_exchange_matrix import get_exchange_matrix
from app.api.get_last_trading_day import get_last_trading_day

def fetch_daily_exchangerates():
    """
    Fetches todays exchange rates for all currencies in the database
    and inserts them into the exchangerate table if they do not already exist.
    """

    # Check last full update
    last_update = fetch_one("SELECT exchangerates FROM status WHERE id = 1")[0]

    if last_update == date.today():
        #print("Exchangerates already updated today, skipping.")
        return

    #print("Fetching today's exchange rates...")

    # Fetch all currencies
    all_currencies = [row[0] for row in fetch_all("SELECT currencycode FROM currency")]

    # Get full exchange matrix for all currencies
    exchange_rates = get_exchange_matrix(all_currencies)

    trading_day = get_last_trading_day()

    # Insert or update all exchange rates
    for pair, rate in exchange_rates.items():
        from_currency, to_currency = pair[:3], pair[3:]
        from_id = get_currency_id_by_code(from_currency)
        to_id = get_currency_id_by_code(to_currency)
        is_calculated = False

        if not from_id or not to_id or not rate:
            # Try to calculate cross-rate using USD as base
            if from_currency != 'USD' and to_currency != 'USD':
                usd_from_rate = exchange_rates.get(f'USD{from_currency}')
                usd_to_rate = exchange_rates.get(f'USD{to_currency}')
                if usd_from_rate and usd_to_rate:
                    calculated_rate = usd_to_rate / usd_from_rate
                    print(f"        🔄 Calculated {pair}: {calculated_rate} (via USD)")
                    # Use calculated rate instead of skipping
                    rate = calculated_rate
                    is_calculated = True
                else:
                    continue
            else:
                continue

        # Upsert logic (pseudo):
        if exchange_rate_exists(from_id, to_id, log_date=trading_day):
            execute_change_query("""
                UPDATE exchangerate
                SET exchangerate = %s
                WHERE fromcurrencyid = %s AND tocurrencyid = %s AND exchangeratelogtime = %s
            """, (rate, from_id, to_id, trading_day))
            if is_calculated:
                print(f"        🔄 Updated {pair}: {rate} (calculated)")
            else:
                print(f"        🔄 Updated {pair}: {rate}")
        else:
            execute_change_query("""
                INSERT INTO exchangerate (fromcurrencyid, tocurrencyid, exchangerate, exchangeratelogtime)
                VALUES (%s, %s, %s, %s)
            """, (from_id, to_id, rate, trading_day))
            if is_calculated:
                print(f"        ➕ Inserted {pair}: {rate} (calculated)")
            else:
                print(f"        ➕ Inserted {pair}: {rate}")

    # Update global status
    execute_change_query("""
        UPDATE status SET exchangerates = %s WHERE id = 1""",
        (date.today(),))