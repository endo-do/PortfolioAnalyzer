from app.database.helpers.fetch_all import fetch_all
from app.database.helpers.fetch_one import fetch_one

def get_bondcategory_totals_by_portfolio(portfolio_id):
    category_rows = fetch_all('SELECT bondcategoryid FROM bondcategory')
    bondcategories = [row[0] for row in category_rows]
    totals = {}
    for bondcategoryid in bondcategories:
        row = fetch_one('SELECT get_bondcategory_value(%s, %s)', (portfolio_id, bondcategoryid))
        totals[bondcategoryid] = row[0] if row else 0
    return totals