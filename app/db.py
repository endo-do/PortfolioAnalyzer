import mysql.connector
from flask_login import UserMixin
from config import DB_CONFIG

def get_db_connection():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT userid, username, userpwd FROM users WHERE userid = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return User(id=result[0], username=result[1], password=result[2])
    return None