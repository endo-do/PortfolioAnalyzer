from config import TWELVE_DATA_KEY

def get_eod_price(queue, symbol, date=None):
    """
    Fetch end-of-day price for a given symbol from Twelve Data API

    Args:
        symbol (str): Ticker symbol of the instrument
        date (str, optional): Date in 'YYYY-MM-DD' format. If None, fetches latest EOD price

    Returns:
        dict: JSON response from the API including 'close' price if successful.
    """
    url = 'https://api.twelvedata.com/eod'
    params = {
        'symbol': symbol,
        'apikey': TWELVE_DATA_KEY
    }
    if date:
        params['date'] = date

    return queue.fetch(url, params)