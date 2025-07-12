from config import TWELVE_DATA_KEY

def get_exchange_rate(queue, symbol, date=None):
    """
    Fetch the current exchange rate of the currencies

    Args:
        symbol (CODE1/CODE2): The conversion of the currencies as a symbol
        date (date, optional): Date of conversion rate. Defaults to None.

    Returns:
        _type_: _description_
    """
    
    url = 'https://api.twelvedata.com/exchange_rate'
    params = {
        'symbol': symbol,
        'apikey': TWELVE_DATA_KEY
    }
    if date:
        params['date'] = date  # format: 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'

    return queue.fetch(url, params)