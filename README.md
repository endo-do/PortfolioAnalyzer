# Portfolio Analyzer  
Portfolio Analyzer is a web application designed to help users analyze and track the value and structure of their securities portfolios in real time.

The project is built using:

- Flask (Python) for the backend logic and API handling  
- MySQL for structured data storage and retrieval  
- HTML/CSS and minimal JavaScript for a simple, functional frontend  

### APIs Used

- Twelve Data API for fetching end-of-day prices, real-time quotes, and exchange rates

## 📋 Project Information

See full [Changelog](CHANGELOG.md) for development progress and updates.

## 🚀 Usage

1. **Install and run a MySQL server** accessible on `localhost` with your own user and password.

2. Create a `.env` file (based on `.env.example`) with your database credentials, Flask secret key, and Twelve Data API key:

3. Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the database setup batch file:

    ```bash
    run_setup.bat
    ```

5. Start the Flask app:

    ```bash
    python run.py
    ```

6. Use the test user to log in:

    - Username: `test`  
    - Password: `12345`
