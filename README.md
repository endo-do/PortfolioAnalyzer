# Portfolio Analyzer  
Portfolio Analyzer is a web application designed to help users analyze and track the value and structure of their securities portfolios in real time.

The project is built using:

    🐍 Flask (Python 3.8+) - Web framework for backend logic and API handling
    🛢️ MySQL - Relational database for structured data storage and retrieval
    🎨 Bootstrap 5 - CSS framework for responsive and modern UI design
    ⚡ JavaScript - Client-side interactivity and dynamic content
    📊 Chart.js - Interactive charts and data visualization
    🔐 Flask-Login - User authentication and session management
    🛡️ Flask-WTF - CSRF protection and form handling
    📝 Jinja2 - Template engine for dynamic HTML generation
    🔄 APScheduler - Background task scheduling for data updates
    📈 yfinance - Financial data API integration
    🧪 pytest - Comprehensive testing framework

## 🔌 APIs Used

    📈 yfinance API for fetching end-of-day prices, real-time quotes, and exchange rates

## 📋 Project Information

See full [Changelog](CHANGELOG.md) for development progress and updates.

## 🚀 Quick Setup

### Prerequisites
- Python 3.8 or higher
- MySQL server running
- Git (to clone the repository)

### Installation Steps

1. **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Portfolio_Analyzer
    ```

2. **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up MySQL server:**
    - Install and start MySQL server
    - Create a user with database creation privileges
    - Note your MySQL credentials (host, username, password)

4. **Create environment configuration:**
    Create a `.env` file in the project root with your database credentials:
    ```env
    DB_HOST=localhost
    DB_USER=your_mysql_username
    DB_PASSWORD=your_mysql_password
    DB_NAME=portfolioanalyzer
    SECRET_KEY=your_secret_key_here
    ```

5. **Run the setup script:**
    ```bash
    python setup.py
    ```
    This will:
    - Create the database
    - Set up all tables
    - Insert default data
    - Create test portfolios

6. **Start the application:**
    ```bash
    python run.py
    ```

7. **Access the application:**
    - Open your browser to: http://localhost:5000
    - Login with admin credentials:
      - Username: `admin`
      - Password: `admin`
    - ⚠️ **Important**: Change the admin password after first login!

## 🧪 Testing

The Portfolio Analyzer includes a comprehensive test suite to ensure reliability and catch issues during development.

#### Quick Start - Run All Tests
```bash
# Run all tests with basic output
python tests/run_tests.py

# Run all tests with detailed output
python tests/run_tests.py -v

# Run all tests with coverage report
python tests/run_tests.py -c

# Run tests in parallel (faster)
python tests/run_tests.py -p
```

#### 🎯 Category-Specific Tests

Run tests for specific functionality:

```bash
# Authentication and security tests
python tests/run_tests.py --auth-only

# Portfolio management tests
python tests/run_tests.py --portfolio-only

# Admin functionality tests
python tests/run_tests.py --admin-only

# API integration tests
python tests/run_tests.py --api-only

# Logging system tests
python tests/run_tests.py --logging-only

# Input validation tests
python tests/run_tests.py --validation-only

# Error handling tests
python tests/run_tests.py --error-handling-only

# Integration workflow tests
python tests/run_tests.py --integration-only
```

#### 📁 Specific Test Files

```bash
# Run a specific test file
python tests/run_tests.py tests/unit/test_auth.py

# Run a specific test class
python tests/run_tests.py tests/unit/test_auth.py::TestUserRegistration

# Run a specific test method
python tests/run_tests.py tests/unit/test_auth.py::TestUserRegistration::test_valid_user_registration
```

#### 🛠️ Alternative: Direct Pytest Commands

```bash
# Run all tests with pytest
python -m pytest tests/ -v

# Run with coverage and HTML report
python -m pytest tests/ --cov=app --cov-report=html

# Run specific test file
python -m pytest tests/unit/test_logging.py -v

# Run tests matching a pattern
python -m pytest tests/ -k "test_logging" -v

# Run tests in parallel
python -m pytest tests/ -n auto
```

### 📊 Understanding Test Results

#### Test Output Symbols:
- **`.`** = Test passed ✅
- **`F`** = Test failed ❌
- **`E`** = Test had an error ⚠️
- **`s`** = Test was skipped ⏭️
- **`x`** = Test was expected to fail but passed 🤔

#### Example Output:
```
tests/unit/test_logging.py::TestLoggingSetup::test_logging_setup_creates_log_files PASSED [  3%]
tests/unit/test_logging.py::TestLoggingSetup::test_logging_setup_creates_log_directory FAILED [  7%]
```
