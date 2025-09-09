from werkzeug.security import generate_password_hash
from app.database.helpers.fetch_one import fetch_one
from app.database.helpers.execute_change_query import execute_change_query

def create_default_admin_user():
    default_password = "admin"
    password_hashed = generate_password_hash(default_password)
    execute_change_query("""
        INSERT INTO user (username, userpwd, email, default_base_currency, is_admin)
        VALUES (%s, %s, %s, %s, %s)
    """, ("admin", password_hashed, "admin@portfolioanalyzer.com", 1, True))
    
    print(f"    ✅ Admin user created successfully")