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

### 🐳 Docker Deployment (Recommended)

**Prerequisites:**
- Docker and Docker Compose installed
- Git (to clone the repository)

**One-Command Setup:**

1. **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Bond-Analyzer
    ```

2. **Create environment file:**
    ```bash
    cp env.example .env
    ```
    Edit `.env` and set your secure passwords:
    ```env
    # Database Configuration
    DB_HOST=db
    DB_USER=portfolio_app
    DB_PASSWORD=your_secure_app_password_here
    DB_NAME=portfolioanalyzer
    DB_ROOT_USER=root
    DB_ROOT_PASSWORD=your_secure_root_password_here
    
    # Flask Secret Key
    SECRET_KEY=your_super_secret_key_here_change_this_in_production
    
    # Admin User Configuration
    ADMIN_PASSWORD=your_secure_admin_password_here
    ```

3. **Start the application:**
    ```bash
    docker-compose up --build
    ```

4. **Access the application:**
    - Open your browser to: http://localhost:5000
    - Login with admin credentials:
      - Username: `admin`
      - Password: `[your ADMIN_PASSWORD from .env]`
    - ⚠️ **Important**: Change the admin password after first login!

**That's it!** The application will automatically:
- Set up the MySQL database
- Create all tables and stored procedures
- Insert default data
- Start the web application

---

### 💻 Local Development Setup

**Prerequisites:**
- Python 3.8 or higher
- MySQL server running
- Git (to clone the repository)

**Installation Steps:**

1. **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Bond-Analyzer
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
    DB_ROOT_USER=root
    DB_ROOT_PASSWORD=your_mysql_root_password
    SECRET_KEY=your_secret_key_here
    ADMIN_PASSWORD=your_admin_password_here
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
      - Password: `[your ADMIN_PASSWORD from .env]`
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

#### 🗄️ Test Database Management

The test suite automatically manages a separate test database (`portfolioanalyzer_test`) that is created and destroyed for each test run:

```bash
# Manually set up test database
python tests/run_tests.py --setup-db

# Manually clean up test database
python tests/run_tests.py --cleanup-db

# Set up database and run tests
python tests/run_tests.py --setup-db --auth-only

# Clean up after running tests
python tests/run_tests.py --portfolio-only --cleanup-db
```

**Note**: The test database is automatically created and cleaned up during normal test runs. Manual management is only needed for debugging or development purposes.

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

## 📁 Project Structure

```
Bond-Analyzer/
├── 📁 app/                          # Main application package
│   ├── 📁 admin/                    # Admin panel functionality
│   │   ├── admin_required.py        # Admin access decorators
│   │   ├── log_viewer.py           # Log file viewing functionality
│   │   ├── routes.py               # Admin routes and endpoints
│   │   └── 📁 templates/           # Admin-specific HTML templates
│   │       ├── admin_dashboard.html
│   │       ├── api_management.html
│   │       ├── currencyoverview.html
│   │       ├── exchangeoverview.html
│   │       ├── log_viewer.html
│   │       ├── securityoverview.html
│   │       ├── securityview_admin.html
│   │       └── useroverview.html
│   │
│   ├── 📁 api/                      # External API integrations
│   │   ├── get_eod_prices.py       # End-of-day price fetching
│   │   ├── get_eod.py              # EOD data processing
│   │   ├── get_exchange_matrix.py  # Exchange rate matrix
│   │   ├── get_exchange.py         # Exchange data retrieval
│   │   ├── get_info.py             # General info API calls
│   │   ├── get_last_trading_day.py # Trading day calculations
│   │   └── routes.py               # API routes
│   │
│   ├── 📁 auth/                     # Authentication system
│   │   ├── routes.py               # Login/register routes
│   │   └── 📁 templates/           # Auth templates
│   │       ├── login.html
│   │       └── register.html
│   │
│   ├── 📁 database/                 # Database layer
│   │   ├── 📁 connection/          # Database connections
│   │   │   ├── cursor.py           # Database cursor management
│   │   │   ├── pool.py             # Connection pooling
│   │   │   └── user.py             # User-specific connections
│   │   │
│   │   ├── 📁 helpers/             # Database helper functions
│   │   │   ├── call_procedure.py   # Stored procedure calls
│   │   │   ├── execute_change_query.py # Data modification queries
│   │   │   ├── fetch_all.py        # Multi-row data fetching
│   │   │   └── fetch_one.py        # Single-row data fetching
│   │   │
│   │   ├── 📁 setup/               # Database initialization
│   │   │   └── setup.py            # Database setup and migration
│   │   │
│   │   └── 📁 tables/              # Table-specific operations
│   │       ├── 📁 api_fetch_logs/  # API logging table
│   │       ├── 📁 bond/            # Bond securities table
│   │       ├── 📁 bondcategory/    # Bond categorization
│   │       ├── 📁 bonddata/        # Bond data storage
│   │       ├── 📁 currency/        # Currency management
│   │       ├── 📁 exchange/        # Exchange information
│   │       ├── 📁 exchangerate/    # Exchange rate data
│   │       ├── 📁 portfolio/       # Portfolio management
│   │       ├── 📁 portfolio_bond/  # Portfolio-bond relationships
│   │       ├── 📁 region/          # Geographic regions
│   │       ├── 📁 sector/          # Industry sectors
│   │       ├── 📁 status/          # Status definitions
│   │       └── 📁 user/            # User management
│   │
│   ├── 📁 static/                   # Static assets
│   │   ├── 📁 css/                 # Stylesheets
│   │   │   └── style.css           # Main application styles
│   │   ├── 📁 js/                  # JavaScript files
│   │   │   ├── currencyoverview.js # Currency page functionality
│   │   │   ├── edit_portfolio.js   # Portfolio editing
│   │   │   ├── exchangeoverview.js # Exchange page functionality
│   │   │   ├── home.js             # Homepage functionality
│   │   │   ├── portfolioview.js    # Portfolio viewing
│   │   │   ├── securitiesview.js   # Securities page
│   │   │   ├── securityoverview.js # Security overview
│   │   │   ├── securityview.js     # Security details
│   │   │   └── useroverview.js     # User management
│   │   └── favicon.ico             # Site favicon
│   │
│   ├── 📁 templates/               # HTML templates
│   │   ├── base.html               # Base template layout
│   │   ├── edit_portfolio.html     # Portfolio editing page
│   │   ├── home.html               # Homepage
│   │   ├── portfolioview.html      # Portfolio viewing page
│   │   ├── securitiesview.html     # Securities listing
│   │   ├── securityview.html       # Security details page
│   │   └── settings.html           # User settings
│   │
│   ├── 📁 utils/                   # Utility functions
│   │   ├── currency_utils.py       # Currency conversion utilities
│   │   ├── formatters.py           # Data formatting functions
│   │   ├── logger.py               # Logging configuration
│   │   └── password_validator.py   # Password validation
│   │
│   ├── __init__.py                 # Flask app initialization
│   └── routes.py                   # Main application routes
│
├── 📁 logs/                        # Application logs
│   ├── errors.log                  # Error logging
│   ├── portfolio_analyzer.log      # General application logs
│   └── security.log                # Security-related logs
│
├── 📁 tests/                       # Test suite
│   ├── 📁 fixtures/                # Test data and fixtures
│   │   ├── __init__.py
│   │   └── test_data.py            # Test data definitions
│   │
│   ├── 📁 unit/                    # Unit tests
│   │   ├── test_admin.py           # Admin functionality tests
│   │   ├── test_api.py             # API integration tests
│   │   ├── test_auth.py            # Authentication tests
│   │   ├── test_error_handling.py  # Error handling tests
│   │   ├── test_input_validation.py # Input validation tests
│   │   ├── test_integration.py     # Integration tests
│   │   ├── test_logging.py         # Logging system tests
│   │   └── test_portfolio.py       # Portfolio functionality tests
│   │
│   ├── conftest.py                 # Pytest configuration
│   ├── database_setup.py           # Test database setup
│   ├── run_tests.py                # Test runner script
│   ├── test_config.py              # Test configuration
│   ├── test_database_connection.py # Database connection tests
│   └── README.md                   # Testing documentation
│
├── 📄 CHANGELOG.md                 # Development history and updates
├── 📄 config.py                    # Application configuration
├── 📄 env.example                  # Environment variables template
├── 📄 README.md                    # This file - project documentation
├── 📄 requirements.txt             # Python dependencies
├── 📄 run.py                       # Application entry point
└── 📄 setup.py                     # Database setup script
```
