from datetime import date
from flask import current_app
from app.database.tables.currency.get_all_currency_pairs import get_all_currency_pairs
from app.database.tables.exchangerate.exchange_rate_exists import exchange_rate_exists
from app.api.get_exchange_rate import get_exchange_rate
from app.database.helpers.execute_change_query import execute_change_query
from app.database.tables.currency.get_currency_code_by_id import get_currency_code_by_id

def fetch_exchangerates():
    """
    Fetches or calculates exchangerate for each currency if none are present in the db
    """

    currency_pairs = get_all_currency_pairs()
    new_rates = {}

    for pair in currency_pairs:
        from_id, to_id = pair

        if exchange_rate_exists(from_id, to_id):
            continue

        if from_id == to_id:
            new_rates[(from_id, to_id)] = 1.0

        elif (to_id, from_id) in new_rates:
            rate = new_rates[(to_id, from_id)]
            new_rates[(from_id, to_id)] = 1 / rate

        else:
            rate_data = get_exchange_rate(
                current_app.api_queue,
                f'{get_currency_code_by_id(from_id)}/{get_currency_code_by_id(to_id)}'
            )
            new_rates[(from_id, to_id)] = rate_data['rate']

    # Insert all collected rates
    for (from_id, to_id), rate in new_rates.items():
        execute_change_query("""
            INSERT INTO exchangerate
                (fromcurrencyid, tocurrencyid, exchangerate, exchangeratelogtime)
                VALUES (%s, %s, %s, %s)
        """, (from_id, to_id, rate, date.today()))