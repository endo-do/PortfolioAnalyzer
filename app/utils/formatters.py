# Data formatters for Portfolio Analyzer - provides percentage and value formatting utilities with proper decimal handling
from decimal import Decimal, ROUND_HALF_UP

def format_percent(value, total):
    # Ensure numeric types for calculation (Decimal or float)
    if not isinstance(value, (Decimal, float, int)):
        value = Decimal(str(value))
    if not isinstance(total, (Decimal, float, int)):
        total = Decimal(str(total))
    if total == 0:
        return '0'  # avoid division by zero
    
    percent = (Decimal(value) / Decimal(total)) * 100
    # Round to nearest integer (half up rounding)
    rounded_percent = percent.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    return str(rounded_percent)  # return as string for easy display with % sign

def format_value(value):
    # Ensure value is Decimal or convert to it
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    # Format with 2 decimal places and comma as thousands separator
    # Adjust decimals as you want, e.g. '0.00'
    formatted = f'{value:,.2f}'
    return formatted