from app.database.helpers.fetch_all import fetch_all

def get_all_users():
    query = """SELECT userid, username, is_admin FROM user"""
    users = fetch_all(query, dictionary=True)
    return users