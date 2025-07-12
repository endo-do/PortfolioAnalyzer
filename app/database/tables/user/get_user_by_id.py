from app.database.helpers.fetch_one import fetch_one
from app.database.connection.user import User

def get_user_by_id(user_id):
    query = 'SELECT userid, username, userpwd, is_admin FROM user WHERE userid = %s'
    result = fetch_one(query, (user_id,))
    if result:
        return User(id=result[0], username=result[1], password=result[2], is_admin=result[3])
    return None
