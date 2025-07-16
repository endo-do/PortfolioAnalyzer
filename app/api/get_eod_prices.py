import yfinance as yf
import pandas as pd

def get_eod_prices(symbols):
    """
    Fetches the latest end-of-day closing prices for a list of symbols using yfinance.
    
    Args:
        symbols (list of str): List of ticker symbols, e.g. ['AAPL', 'MSFT']
        
    Returns:
        dict: Mapping of symbol to closing price (float). If no data, value is None.
    """
    if not symbols:
        return {}

    # Download last 1 day of data for all symbols
    data = yf.download(symbols, period="1d", group_by='ticker', threads=True, progress=False, auto_adjust=True)
    
    prices = {}

    # When multiple symbols: data is a multi-level dataframe with symbol keys
    if isinstance(data.columns, pd.MultiIndex):
        for symbol in symbols:
            try:
                close_price = data[symbol]['Close'][-1]
                prices[symbol] = float(close_price) if not pd.isna(close_price) else None
            except KeyError:
                prices[symbol] = None
    else:
        # Single symbol case: columns are just ['Open', 'Close', ...]
        close_price = data['Close'][-1]
        prices[symbols[0]] = float(close_price) if not pd.isna(close_price) else None

    return prices
