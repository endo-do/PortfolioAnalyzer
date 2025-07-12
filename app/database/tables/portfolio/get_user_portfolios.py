from app.database.helpers.fetch_all import fetch_all
from app.database.tables.portfolio.get_portfolio import get_portfolio

def get_user_portfolios(userid):
    portfolio_ids = fetch_all("""SELECT portfolioid from portfolio where userid = %s""", (userid,))
    portfolios = []
    for portfolio_id in portfolio_ids:
        portfolios.append(get_portfolio(portfolio_id[0]))

    return portfolios