from app.database.helpers.fetch_one import fetch_one
from datetime import date

def exchange_rate_exists(from_currency_id, to_currency_id, log_date=None):
    """
    Check if an exchange rate record exists for given currencies on a given date.

    Args:
        from_currency_id (int): Base currency ID
        to_currency_id (int): Quote currency ID
        log_date (date, optional): Date to check. Defaults to today.

    Returns:
        bool: True if record exists, else False
    """
    if log_date is None:
        log_date = date.today()

    query = """
        SELECT 1 FROM exchangerate
        WHERE fromcurrencyid = %s AND tocurrencyid = %s
        AND exchangeratelogtime = %s
        LIMIT 1
    """
    args = (from_currency_id, to_currency_id, log_date)
    result = fetch_one(query=query, args=args)
    
    return result is not None