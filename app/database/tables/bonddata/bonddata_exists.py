from app.database.helpers.fetch_one import fetch_one
from datetime import date

def bonddata_exists(bondid, log_date):
    """
    Check if a bonddata record exists for given security on a given date.

    Args:
        bondid (int): Bond ID
        log_date (date, optional): Date to check. Defaults to today.

    Returns:
        bool: True if record exists, else False
    """

    query = """
        SELECT 1 FROM bonddata
        WHERE bondid = %s
        AND bonddatalogtime = %s
        LIMIT 1
    """
    args = (bondid, log_date)
    result = fetch_one(query=query, args=args)
    
    return result is not None