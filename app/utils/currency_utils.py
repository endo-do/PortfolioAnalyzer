from app.database.tables.currency.get_currency_code_by_id import get_currency_code_by_id

def get_user_default_currency(user):
    """
    Get the user's default currency code.
    
    Args:
        user: The current user object
        
    Returns:
        str: The user's default currency code (e.g., 'USD', 'CHF', 'EUR')
    """
    if hasattr(user, 'default_base_currency') and user.default_base_currency:
        currency_code = get_currency_code_by_id(user.default_base_currency)
        return currency_code if currency_code else 'USD'
    return 'USD'
