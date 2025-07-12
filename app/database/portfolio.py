from app.database.db import fetch_all, fetch_one, call_procedure
from flask_login import current_user
from utils.formatters import format_percent, format_value

def get_bondcategory_totals_by_portfolio(portfolio_id):
    category_rows = fetch_all('SELECT bondcategoryid FROM bondcategories')
    bondcategories = [row[0] for row in category_rows]
    totals = {}
    for bondcategoryid in bondcategories:
        row = fetch_one('SELECT get_bondcategory_value(%s, %s)', (portfolio_id, bondcategoryid))
        totals[bondcategoryid] = row[0] if row else 0
    return totals

def get_portfolio_by_id(portfolio_id):
    query = """
        SELECT portfolioname, portfoliodescription, currencycode 
        FROM portfolios p JOIN currencies c on c.currencyid = p.portfoliocurrencyid
        WHERE portfolioid = %s;"""
    args = (portfolio_id,)
    portfolio = fetch_one(query, args, dictionary=True)
    return portfolio

def get_portfolio_bonds(portfolio_id):
    query = """
            SELECT b.symbol, b.bondname, bc.bondcategoryname, bd.bondrate, bd.bonddatalogtime, pb.quantity, c.currencycode
            FROM bonds b
            JOIN bondcategories bc USING (bondcategoryid)
            JOIN bonddata bd ON b.bondid = bd.bondid
            JOIN (
                SELECT bondid, MAX(bonddatalogtime) AS maxlogtime
                FROM bonddata
                GROUP BY bondid
            ) latest ON bd.bondid = latest.bondid AND bd.bonddatalogtime = latest.maxlogtime
            JOIN portfolios_bonds pb ON b.bondid = pb.bondid
            JOIN currencies c ON c.currencyid = b.bondcurrencyid
            WHERE pb.portfolioid = %s
            """
    args = (portfolio_id,)
    bonds = fetch_all(query, args, dictionary=True)
    return bonds

def get_user_portfolios(userid):
    portfolios = call_procedure("get_user_portfolios", (userid,), dictionary=True)
    portfolios_dict = {}
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

        portfolios_dict[portfolio_id] = portfolio

    return portfolios_dict

def get_portfolio_detailed(portfolio_id):
    portfolio = get_portfolio_by_id(portfolio_id)
    user_portfolios = get_user_portfolios(current_user.id)
    portfolio = portfolio | user_portfolios[portfolio_id]
    return portfolio