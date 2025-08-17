from app.database.helpers.execute_change_query import execute_change_query
from app.database.helpers.fetch_one import fetch_one

def insert_sectors():
    """
    Inserts sectors with GICS names as sectorname and Yahoo Finance labels as sectordisplayname.
    """
    sectors = [
        ("Basic Materials", "Basic Materials"),
        ("Communication Services", "Communication Services"),
        ("Consumer Cyclical", "Consumer Cyclical"),
        ("Consumer Defensive", "Consumer Defensive"),
        ("Energy", "Energy"),
        ("Financial Services", "Financial Services"),
        ("Healthcare", "Healthcare"),
        ("Industrials", "Industrials"),
        ("Real Estate", "Real Estate"),
        ("Technology", "Technology"),
        ("Utilities", "Utilities"),
        ("N/A", "Undefined"),
    ]

    query = """
    INSERT INTO sector (sectorname, sectordisplayname)
    VALUES (%s, %s)
    """

    for sectorname, displayname in sectors:
        # Avoid duplicate inserts
        existing = fetch_one("SELECT sectorid FROM sector WHERE sectorname = %s", (sectorname,))
        if not existing:
            execute_change_query(query, (sectorname, displayname))