from app.database.helpers.execute_change_query import execute_change_query
from app.database.helpers.fetch_one import fetch_one

def insert_regions():
    """
    Inserts all the regions.
    """
    regions = [
        "North America",
        "Europe",
        "South America",
        "Asia",
        "Africa",
        "Middle East",
        "Oceania",
        "Other",
    ]

    query = """
    INSERT INTO region (region)
    VALUES (%s)
    """

    for region in regions:
        execute_change_query(query, (region,))
    
    print(f"    ✅ Regions inserted successfully")