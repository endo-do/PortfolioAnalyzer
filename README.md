# Portfolio Analyzer  
Portfolio Analyzer is a web application designed to help users analyze and track the value and structure of their securities portfolios in real time.

The project is built using:

    🐍 Flask (Python) for the backend logic and API handling

    🛢️ MySQL for structured data storage and retrieval

    🖥️ HTML/CSS with Bootstrap and minimal JavaScript for a simple, clean, and functional frontend design

## 🔌 APIs Used

    📈 yfinance API for fetching end-of-day prices, real-time quotes, and exchange rates

## 📋 Project Information

See full [Changelog](CHANGELOG.md) for development progress and updates.

## 🚀 Usage

1. **Install and run a MySQL server** accessible on `localhost` with your own user and password.

2. Create a `.env` file (based on `.env.example`) with your database credentials and a Flask secret key:

3. Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the database setup file from the project root folder:

    ```bash
    python -m app.database.setup.setupt
    ```

5. Start the Flask app:

    ```bash
    python run.py
    ```

6. Users and Access

    Admin user:

        Username: admin

        Password: admin

        Role: Has full access including the admin endpoint used for Security, Currency and User-Management.
   

8. Create your own users and portfolios to fully customize your experience.  
   Have fun exploring and managing your securities!

   If you encounter any problems or have questions, feel free to contact me.
