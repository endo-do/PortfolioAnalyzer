from app.database.connection import get_db_connection, release_db_connection, User
from utils.formatters import format_percent, format_value

def get_user_by_id(user_id):
    """
    get user details from db based on userid

    Args:
        user_id (int): user id

    Returns:
        User: User class, None if no matching user was found
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT userid, username, userpwd FROM users WHERE userid = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    release_db_connection(conn)

    if result:
        return User(id=result[0], username=result[1], password=result[2])
    return None

def get_all_currency_pairs():
    """
    Returns all distinct pairs of currencies

    Returns:
        list: list of all distinct pairs
    """
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT currencyid FROM currencies")
    currencies = [row[0] for row in cursor.fetchall()]
    pairs = []
    for base in currencies:
        for quote in currencies:
            pairs.append((base, quote))
    cursor.close()
    release_db_connection(conn)
    
    return pairs

def get_currency_code_by_id(currency_id):
    """
    Returns currency code based on its id in the database

    Args:
        currency_id (int): currencyid
    
    Returns:
        str: currency code or None
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT currencycode FROM currencies
        WHERE currencyid = %s
    """, (currency_id,))
    result = cursor.fetchone()
    cursor.close()
    release_db_connection(conn)

    return result[0] if result else None

def get_user_portfolios(userid):
    """
    Returns all portfolios of a user with basic informations

    Args:
        userid (int): userid

    Returns:
        list: list of portfolios as dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc("get_user_portfolios", (userid,))
    portfolios = []
    
    for result in cursor.stored_results():
        portfolios.extend(result.fetchall())
    
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

    cursor.close()
    release_db_connection(conn)
    return portfolios

def get_bondcategory_totals_by_portfolio(portfolio_id):
    """
    Returns total value for each bondcategory in portfolio

    Args:
        portfolio_id (int): portfolio id

    Returns:
        dict: dictionary with the bondcategories and their total value
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT bondcategoryid FROM bondcategories")
    bondcategories = [row[0] for row in cursor.fetchall()]

    totals = {}
    for bondcategoryid in bondcategories:
        cursor.callproc('get_bondcategory_value', (portfolio_id, bondcategoryid))
        
        total_value = None
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                total_value = row[0]
            else:
                total_value = 0
        
        totals[bondcategoryid] = total_value

    return totals

def get_distinct_user_bond_isins(userid):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""CALL get_user_distinct_bond_isins(%s)""", (userid,))
    
    bonds = {row[0]: row[1] for row in cursor.fetchall()}  # {id: isin}
    cursor.close()
    release_db_connection(conn)
    return bonds