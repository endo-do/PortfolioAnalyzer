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

4. Run the database setup batch file from the project root folder:

    ```bash
    .\sql\setup\run_setup.bat
    ```

5. Start the Flask app:

    ```bash
    python run.py
    ```

6. Initial Testing Users

For initial testing, use one of the following accounts:

    Admin user:
    Username: admin
    Password: admin

    Regular user:
    Username: testuser
    Password: test

7. Create your own users and portfolios to fully customize your experience.  
   Have fun exploring and managing your securities!

   If you encounter any problems or have questions, feel free to contact me.
