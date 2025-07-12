from app.database.helpers.fetch_one import fetch_one

def exchange_rate_exists(from_currency_id, to_currency_id):
    """
    Check if an exchange rate record exists for given currencies

    Args:
        cursor: Database cursor
        from_currency_id (int): currencyid of base currency
        to_currency_id (int): currencyid of quote currency

    Returns:
        bool: True if record exists, else False
    """
    query = """
        SELECT 1 FROM exchangerate
        WHERE fromcurrencyid = %s AND tocurrencyid = %s
        LIMIT 1
    """
    args = (from_currency_id, to_currency_id)
    result = fetch_one(query=query, args=args)
    
    return result is not None