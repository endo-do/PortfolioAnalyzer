from app.database.helpers.execute_change_query import execute_change_query

def add_api_fetch_logs_table():
    """
    Create the api_fetch_logs table if it doesn't exist.
    
    Returns:
        bool: True if table was created successfully or already exists, False otherwise
    """
    try:
        # Create the table using the SQL from create_api_fetch_logs.sql
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS api_fetch_logs (
            id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            symbol VARCHAR(20) NOT NULL,
            fetch_type ENUM('STOCK', 'EXCHANGE') NOT NULL,
            status ENUM('SUCCESS', 'FAILED', 'PENDING', 'PARTIAL') NOT NULL DEFAULT 'PENDING',
            error_message TEXT,
            fetch_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            retry_count INT NOT NULL DEFAULT 0,
            INDEX idx_symbol (symbol),
            INDEX idx_fetch_type (fetch_type),
            INDEX idx_status (status),
            INDEX idx_fetch_time (fetch_time)
        )
        """
        
        execute_change_query(create_table_sql)
        return True
        
    except Exception as e:
        print(f"Failed to create api_fetch_logs table: {e}")
        return False
