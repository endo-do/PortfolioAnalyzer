from app.database.get_data import fetch_one, fetch_all, call_procedure
from app.database.connection import User
from utils.formatters import format_percent, format_value
from app.database.portfolio_data import get_bondcategory_totals_by_portfolio


def get_user_by_id(user_id):
    query = 'SELECT userid, username, userpwd, is_admin FROM users WHERE userid = %s'
    result = fetch_one(query, (user_id,))
    if result:
        return User(id=result[0], username=result[1], password=result[2], is_admin=result[3])
    return None

def get_user_portfolios(userid):
    portfolios = call_procedure("get_user_portfolios", (userid,), dictionary=True)
    for portfolio in portfolios:
        portfolio_id = portfolio["portfolioid"]
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

    return portfolios

def get_distinct_user_bond_isins(userid):
    rows = call_procedure("get_user_distinct_bond_isins", (userid,))
    return {row[0]: row[1] for row in rows}