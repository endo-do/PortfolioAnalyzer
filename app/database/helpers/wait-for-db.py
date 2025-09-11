# Database connection waiter for Portfolio Analyzer - waits for MySQL database to be ready before starting web app
import socket, sys, time, os

# Add the app directory to Python path to import config
sys.path.insert(0, '/app')

import mysql.connector
from config import DB_CONFIG, DB_ROOT_CONFIG

host = sys.argv[1]
port = int(sys.argv[2])

print(f"Waiting for database at {host}:{port}...")

# First, wait for the port to be open
while True:
    try:
        s = socket.create_connection((host, port), 2)
        s.close()
        print(f"✅ Port {host}:{port} is open")
        break
    except Exception as e:
        print(f"⏳ Waiting for {host}:{port}... {e}")
        time.sleep(1)

# Then, wait for MySQL to be ready to accept connections with proper authentication
max_attempts = 30
attempt = 0

while attempt < max_attempts:
    try:
        # Try to connect with root credentials to verify MySQL is fully ready
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=DB_ROOT_CONFIG['user'],
            password=DB_ROOT_CONFIG['password'],
            connection_timeout=5
        )
        conn.close()
        print(f"✅ MySQL server is ready and accepting authenticated connections")
        break
    except mysql.connector.Error as e:
        attempt += 1
        if attempt < max_attempts:
            print(f"⏳ MySQL not ready yet (attempt {attempt}/{max_attempts}): {e}")
            time.sleep(2)
        else:
            print(f"❌ MySQL connection failed after {max_attempts} attempts: {e}")
            print("💡 Make sure your DB_ROOT_PASSWORD in .env file is correct")
            sys.exit(1)
    except Exception as e:
        attempt += 1
        if attempt < max_attempts:
            print(f"⏳ Unexpected error (attempt {attempt}/{max_attempts}): {e}")
            time.sleep(2)
        else:
            print(f"❌ Unexpected error after {max_attempts} attempts: {e}")
            sys.exit(1)

print("🚀 MySQL server is ready - proceeding with application startup")