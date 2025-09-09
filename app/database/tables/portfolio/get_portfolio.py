from flask_login import current_user
from app.database.helpers.call_procedure import call_procedure
from app.database.tables.bondcategory.get_bondcategory_totals_by_portfolio import get_bondcategory_totals_by_portfolio
from app.utils.formatters import format_percent
from app.database.helpers.fetch_all import fetch_all
from app.database.tables.portfolio.get_sector_breakdown import get_sector_breakdown
from app.database.tables.portfolio.get_region_breakdown import get_region_breakdown

def get_portfolio(portfolio_id):
    portfolio = call_procedure("get_portfolio", (portfolio_id,), dictionary=True)[0]
    # Hole bondcategoryid und bondcategoryname aus DB
    categories = fetch_all("SELECT bondcategoryid, bondcategoryname FROM bondcategory", dictionary=True)
    # categories: [{'bondcategoryid': 1, 'bondcategoryname': 'etfs'}, ...]

    # Hole totals (bondcategoryid => sum)
    bondcategory_totals = get_bondcategory_totals_by_portfolio(portfolio_id)
    total_value = portfolio.get('total_value') or 0
    # Convert decimal.Decimal to float to avoid TypeError in templates
    total_value = float(total_value) if total_value is not None else 0.0
    total_for_percent = total_value if total_value != 0 else 1

    portfolio['total_value'] = total_value

    # Erstelle Mapping bondcategoryid -> bondcategoryname
    category_map = {cat['bondcategoryid']: cat['bondcategoryname'].lower() for cat in categories}

    # Für jede Kategorie Wert und Prozent mit aussagekräftigem Namen ins portfolio dict
    for cat_id, cat_name in category_map.items():
        value = bondcategory_totals.get(cat_id) or 0
        portfolio[f'{cat_name}_value'] = value
        portfolio[f'{cat_name}_percent'] = format_percent(value, total_for_percent)

    sectors =  get_sector_breakdown(portfolio_id)
    portfolio.update(sectors)

    regions = get_region_breakdown(portfolio_id)
    portfolio.update(regions)

    return portfolio