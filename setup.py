#!/usr/bin/env python3
"""
Portfolio Analyzer Setup Script

This script sets up the Portfolio Analyzer application by:
1. Creating the database
2. Running all SQL table creation scripts
3. Inserting default data
4. Creating test data

Prerequisites:
- MySQL server running
- .env file with database configuration
- Python dependencies installed (pip install -r requirements.txt)

Usage:
    python setup.py
"""

import os
import sys
from pathlib import Path

def check_prerequisites():
    """Check if all prerequisites are met."""
    print("🔍 Checking prerequisites...")
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found!")
        print("   Please create a .env file with your database configuration:")
        print("   DB_HOST=localhost")
        print("   DB_USER=your_username")
        print("   DB_PASSWORD=your_password")
        print("   DB_NAME=portfolioanalyzer")
        print("   SECRET_KEY=your_secret_key")
        print("\n   Example .env file:")
        print("   DB_HOST=localhost")
        print("   DB_USER=root")
        print("   DB_PASSWORD=mypassword")
        print("   DB_NAME=portfolioanalyzer")
        print("   SECRET_KEY=my-secret-key-123")
        return False
    
    # Check if config can be loaded
    try:
        from config import DB_CONFIG
        if not all([DB_CONFIG['host'], DB_CONFIG['user'], DB_CONFIG['password']]):
            print("❌ Database configuration incomplete in .env file")
            print("   Required: DB_HOST, DB_USER, DB_PASSWORD")
            return False
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return False
    
    # Check if MySQL connector is available
    try:
        import mysql.connector
    except ImportError:
        print("❌ mysql-connector-python not installed!")
        print("   Run: pip install mysql-connector-python")
        return False
    
    print("✅ Prerequisites check passed")
    return True

def main():
    """Main setup function."""
    print("🚀 Portfolio Analyzer Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Setup failed - please fix the issues above and try again")
        sys.exit(1)
    
    # Run the database setup
    try:
        from app.database.setup.setup import main as setup_database
        setup_database()
        print("\n🎉 Setup completed successfully!")
        
        # Check if running in Docker or locally
        is_docker = os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true'
        
        # Get network configuration from environment
        host_ip = os.environ.get('HOST_IP', 'localhost')
        port = os.environ.get('PORT', '5000')
        
        print("\n🐳 Docker Deployment:")
        print("✅ Database setup complete - application is ready!")
        print(f"🌐 Access your application at: http://{host_ip}:{port}")
        print("🔑 Admin credentials:")
        print("   Username: admin")
        print("   Password: [from your .env ADMIN_PASSWORD]")
        print("   ⚠️  IMPORTANT: Change this password after first login!")
        print()
        
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        print("\nTroubleshooting:")
        print("- Make sure MySQL server is running")
        print("- Check your database credentials in .env file")
        print("- Ensure you have permission to create databases")
        sys.exit(1)

if __name__ == '__main__':
    main()
