from app.database.helpers.execute_change_query import execute_change_query

def insert_initial_update_status():
    query = """
        INSERT INTO status (exchangerates, securities, system_generated)
        VALUES (%s, %s, %s)
    """
    execute_change_query(query, (None, None, None))
