from flask_login import current_user
from app.database.helpers.call_procedure import call_procedure
from app.database.tables.bondcategory.get_bondcategory_totals_by_portfolio import get_bondcategory_totals_by_portfolio
from app.utils.formatters import format_percent, format_value

def get_portfolio(portfolio_id):
    portfolio = call_procedure("get_portfolio", (portfolio_id,), dictionary=True)[0]

    bondcategory_totals = get_bondcategory_totals_by_portfolio(portfolio_id)

    portfolio['etfs_value'] = bondcategory_totals[1] if bondcategory_totals[1] is not None else 0
    portfolio['shares_value'] = bondcategory_totals[2] if bondcategory_totals[2] is not None else 0
    portfolio['funds_value'] = bondcategory_totals[3] if bondcategory_totals[3] is not None else 0
    portfolio['bonds_value'] = bondcategory_totals[4] if bondcategory_totals[4] is not None else 0

    # Keep raw total as a number (Decimal or float), don't format yet
    raw_total = portfolio['total_value'] if portfolio['total_value'] is not None else 0

    # Use raw_total for percentage calculations, prevent division by zero
    total_for_percent = raw_total if raw_total != 0 else 1

    # Calculate percents using raw numeric values
    portfolio['etfs_percent'] = format_percent(portfolio['etfs_value'], total_for_percent)
    portfolio['shares_percent'] = format_percent(portfolio['shares_value'], total_for_percent)
    portfolio['funds_percent'] = format_percent(portfolio['funds_value'], total_for_percent)
    portfolio['bonds_percent'] = format_percent(portfolio['bonds_value'], total_for_percent)

    # Now format values for display (convert to strings)
    portfolio['total_value'] = format_value(raw_total)
    portfolio['etfs_value'] = format_value(portfolio['etfs_value'])
    portfolio['shares_value'] = format_value(portfolio['shares_value'])
    portfolio['funds_value'] = format_value(portfolio['funds_value'])
    portfolio['bonds_value'] = format_value(portfolio['bonds_value'])

    return portfolio