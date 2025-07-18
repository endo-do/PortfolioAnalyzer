from app.database.helpers.fetch_all import fetch_all


def get_all_categories():
    query = """SELECT bondcategoryid, bondcategoryname FROM bondcategory"""
    categories = fetch_all(query=query, dictionary=True)
    return categories