from app.database.helpers.fetch_one import fetch_one
from app.database.connection.user import User

def get_user_by_id(user_id):
    query = 'SELECT userid, username, userpwd, email, default_base_currency, is_admin, created_at FROM user WHERE userid = %s'
    result = fetch_one(query, (user_id,), dictionary=True)
    if result:
        return User(
            id=result['userid'], 
            username=result['username'], 
            password=result['userpwd'],
            email=result.get('email', 'N/A'),
            default_base_currency=result.get('default_base_currency', 1),
            is_admin=result['is_admin'],
            created_at=result.get('created_at')
        )
    return None
