import yfinance as yf
from itertools import permutations

def get_exchange_matrix(currencies: list) -> dict:
    """
    Fetch today's exchange rates for all permutations of the given currencies.
    Returns a dictionary like {'USDCHF': 0.89, 'CHFUSD': 1.12, ...}
    """
    if len(currencies) > 10:
        raise ValueError("Maximum 10 currencies allowed")

    pairs = list(permutations(currencies, 2))  # e.g., [('USD', 'CHF'), ('CHF', 'USD'), ...]
    symbols = [f"{a}{b}=X" for a, b in pairs]

    # Download all at once for today's data
    data = yf.download(symbols, period="1d", group_by='ticker', threads=True, progress=False)

    exchange_rates = {}
    for (a, b), symbol in zip(pairs, symbols):
        try:
            rate = data[symbol]["Close"].dropna().iloc[-1]
            exchange_rates[f"{a}{b}"] = rate
        except Exception:
            exchange_rates[f"{a}{b}"] = None  # If data is missing

    return exchange_rates