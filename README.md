# Portfolio Analyzer  
A modern web application for portfolio management and analysis, built with Docker for easy deployment. Track your securities investments across multiple portfolios with real-time data, interactive charts, and comprehensive analytics. Features include multi-currency support, sector/regional breakdowns, and secure user authentication. Deploy with a single command using Docker Compose - no complex setup required.

The project is built using:

    🐳 Docker & Docker Compose - Containerization and orchestration for easy deployment
    🐍 Flask (Python 3.8+) - Web framework for backend logic and API handling
    🛢️ MySQL - Relational database for structured data storage and retrieval
    🎨 Bootstrap 5 - CSS framework for responsive and modern UI design
    ⚡ JavaScript - Client-side interactivity and dynamic content
    📊 Chart.js - Interactive charts and data visualization
    🔐 Flask-Login - User authentication and session management
    🛡️ Flask-WTF - CSRF protection and form handling
    📝 Jinja2 - Template engine for dynamic HTML generation
    🔄 APScheduler - Background task scheduling for data updates
    🧪 pytest - Comprehensive testing framework

## 🔌 APIs Used

    📈 yfinance API for fetching end-of-day prices, real-time quotes, and exchange rates

## 📋 Project Information

See full [Changelog](CHANGELOG.md) for development progress and updates.

## 🚀 Quick Setup

### 🐳 Docker Deployment

**Prerequisites:**
- Docker and Docker Compose installed
- Git (to clone the repository)

**One-Command Setup:**

1. **Clone the repository:**
    ```bash
    # All platforms (requires Git)
    git clone https://github.com/endo-do/PortfolioAnalyzer.git
    cd PortfolioAnalyzer
    ```

2. **Create environment file:**
    ```bash
    # Unix/Linux/macOS/Git Bash
    cp env.example .env
    
    # Windows Command Prompt
    copy env.example .env
    
    # Windows PowerShell
    Copy-Item env.example .env
    ```

3. **Edit the environment file:**
    ```bash
    # Unix/Linux/macOS/Git Bash
    nano .env
    # or
    vim .env
    
    # Windows Command Prompt
    notepad .env
    
    # Windows PowerShell
    notepad .env
    # or
    code .env  # if VS Code is installed
    ```
    
    Set your secure passwords in the `.env` file:
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
    
    # Network Configuration (optional)
    HOST_IP=0.0.0.0    # Use your computer's IP or localhost
    PORT=5000          # Port to expose the application
    ```

4. **Start the application:**
    ```bash
    # All platforms (requires Docker)
    docker-compose up --build
    ```

5. **Access the application:**
    - **From your computer:** http://localhost:5000
    - **From your phone/other devices if set up:** http://[YOUR_IP]:5000
    - Login with admin credentials:
      - Username: `admin`
      - Password: `[your ADMIN_PASSWORD from .env]`
    - ⚠️ **Important**: Change the admin password after first login!

**That's it!** The application will automatically:
- Set up the MySQL database
- Create all tables and stored procedures
- Insert default data
- Start the web application

#### 🛑 Stopping and Cleaning Up

**Stop the application:**
```bash
docker-compose down
```

**Stop and remove all data (fresh start):**
```bash
docker-compose down
docker volume rm bond-analyzer_db_data
docker-compose up --build
```

**Complete cleanup (remove everything):**
```bash
docker-compose down
docker volume rm bond-analyzer_db_data
docker rmi bond-analyzer_web
```

## 🧪 Testing

The Portfolio Analyzer includes a comprehensive test suite to ensure reliability and catch issues during development. The test suite uses a separate test database with automatic setup and cleanup.

#### Quick Start - Run All Tests

```bash
# Run all tests with automatic database setup
docker-compose exec web python tests/run_tests.py --setup-db -v
```

> **💡 Tip:** The `--setup-db` flag automatically drops and recreates the test database, ensuring a clean test environment with proper permissions. Use `--verbose-db` to see detailed database setup logs.

#### 🎯 Category-Specific Tests

Run tests for specific functionality:

```bash
# Authentication and security tests
docker-compose exec web python tests/run_tests.py --setup-db --auth-only -v

# Portfolio management tests
docker-compose exec web python tests/run_tests.py --setup-db --portfolio-only -v

# Admin functionality tests
docker-compose exec web python tests/run_tests.py --setup-db --admin-only -v

# API integration tests
docker-compose exec web python tests/run_tests.py --setup-db --api-only -v

# Logging system tests
docker-compose exec web python tests/run_tests.py --setup-db --logging-only -v

# Input validation tests
docker-compose exec web python tests/run_tests.py --setup-db --validation-only -v

# Error handling tests
docker-compose exec web python tests/run_tests.py --setup-db --error-handling-only -v

# Integration workflow tests
docker-compose exec web python tests/run_tests.py --setup-db --integration-only -v
```

#### 📁 Specific Test Files

```bash
# Run a specific test file
docker-compose exec web python tests/run_tests.py --setup-db tests/unit/test_auth.py -v

# Run a specific test class
docker-compose exec web python tests/run_tests.py --setup-db tests/unit/test_auth.py::TestUserRegistration -v

# Run a specific test method
docker-compose exec web python tests/run_tests.py --setup-db tests/unit/test_auth.py::TestUserRegistration::test_valid_user_registration -v
```

### 📊 Understanding Test Results

#### Test Output Symbols:
- **`.`** = Test passed ✅
- **`F`** = Test failed ❌
- **`E`** = Test had an error ⚠️
- **`s`** = Test was skipped ⏭️
- **`x`** = Test was expected to fail but passed 🤔

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
│   │   │   ├── wait-for-db.py  # Database connection wait script
│   │   │   ├── execute_change_query.py # Data modification queries
│   │   │   ├── fetch_all.py        # Multi-row data fetching
│   │   │   ├── fetch_one.py        # Single-row data fetching
│   │   │   └── wait-for-db.py      # Database connection wait script
│   │   │
│   │   ├── 📁 setup/               # Database initialization
│   │   │   ├── create_app_user.sql # Application user creation script
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
├── 📄 docker-compose.yml           # Docker Compose configuration
├── 📄 Dockerfile                   # Docker image definition
├── 📄 env.example                  # Environment variables template
├── 📄 README.md                    # This file - project documentation
├── 📄 requirements.txt             # Python dependencies
├── 📄 run.py                       # Application entry point
├── 📄 setup.py                     # Database setup script
└── 📄 wsgi.py                      # WSGI entry point for production
```
<br />
<br />
vibecoding works, thx cursor :pray:
