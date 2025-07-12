from app.database.connection.cursor import db_cursor


def fetch_one(query, args=None, dictionary=False):
    args = args or ()
    with db_cursor(dictionary=dictionary) as cursor:
        cursor.execute(query, args)
        return cursor.fetchone()