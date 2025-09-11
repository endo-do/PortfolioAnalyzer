from werkzeug.security import generate_password_hash
from app.database.helpers.fetch_one import fetch_one
from app.database.helpers.execute_change_query import execute_change_query
from config import ADMIN_PASSWORD, ADMIN_EMAIL

def create_default_admin_user():
    # Get admin password from configuration
    admin_password = ADMIN_PASSWORD
    
    # Check if admin user already exists
    existing_admin = fetch_one("SELECT userid FROM user WHERE username = %s", ("admin",))
    if existing_admin:
        print(f"    ℹ️  Admin user already exists, skipping creation")
        return
    
    password_hashed = generate_password_hash(admin_password)
    execute_change_query("""
        INSERT INTO user (username, userpwd, email, default_base_currency, is_admin)
        VALUES (%s, %s, %s, %s, %s)
    """, ("admin", password_hashed, ADMIN_EMAIL, 1, True))
    
    print(f"    ✅ Admin user created successfully")