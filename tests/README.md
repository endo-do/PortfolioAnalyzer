# Portfolio Analyzer Test Suite

This directory contains comprehensive tests for the Portfolio Analyzer application.

## Test Structure

```
tests/
├── conftest.py                 # Test configuration and fixtures
├── run_tests.py               # Test runner script
├── README.md                  # This file
├── fixtures/
│   ├── __init__.py
│   └── test_data.py           # Test data fixtures
└── unit/
    ├── __init__.py
    ├── test_auth.py           # Authentication tests
    ├── test_portfolio.py      # Portfolio management tests
    ├── test_admin.py          # Admin functionality tests
    ├── test_api.py            # API endpoint tests
    ├── test_logging.py        # Logging system tests
    ├── test_integration.py    # Integration tests
    ├── test_input_validation.py # Input validation tests
    └── test_error_handling.py # Error handling tests
```

## Test Categories

### 1. Authentication Tests (`test_auth.py`)
- User registration with valid/invalid data
- User login with valid/invalid credentials
- Password strength validation
- CSRF protection
- Session management
- Input validation and sanitization

### 2. Portfolio Management Tests (`test_portfolio.py`)
- Portfolio creation, editing, deletion
- Portfolio viewing and access control
- Securities management
- Data validation
- Ownership verification

### 3. Admin Functionality Tests (`test_admin.py`)
- Admin access control
- Security management
- Currency management
- Exchange management
- User management
- Log viewer functionality

### 4. API Endpoint Tests (`test_api.py`)
- EOD price API
- Exchange rate API
- Security information API
- Error handling
- Authentication and authorization

### 5. Logging System Tests (`test_logging.py`)
- Logging setup and configuration
- User action logging
- Security event logging
- Error logging
- Log file rotation
- Log viewer functionality

### 6. Integration Tests (`test_integration.py`)
- Complete user workflows
- Portfolio management workflows
- Admin management workflows
- API integration workflows
- Error handling workflows

### 7. Input Validation Tests (`test_input_validation.py`)
- SQL injection protection
- XSS protection
- Path traversal protection
- Input length validation
- Input format validation
- Required field validation
- Data type validation
- Boundary value validation

### 8. Error Handling Tests (`test_error_handling.py`)
- Database error handling
- API error handling
- File system error handling
- Network error handling
- Memory error handling
- Permission error handling
- Validation error handling
- Concurrency error handling
- Recovery mechanisms

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install pytest pytest-cov pytest-xdist pytest-flask
```

### Test Database Setup

The test suite uses a separate test database (`portfolioanalyzer_test`) to avoid interfering with your production data. The test database is automatically managed and uses root database credentials for full permissions.

#### Database Setup Options

**Automatic Setup (Recommended):**
```bash
python tests/run_tests.py --setup-db
```
This flag:
- **Drops** the existing test database (if it exists)
- **Creates** a fresh test database
- **Sets up** all required tables, triggers, and procedures
- **Inserts** minimal test data
- **Runs** the tests with a clean database environment

**Manual Setup:**
If you prefer to manage the test database manually:
```bash
# Create test database
python tests/database_setup.py

# Run tests without automatic setup
python tests/run_tests.py
```

### Basic Test Execution

Run all tests with automatic database setup:
```bash
python tests/run_tests.py --setup-db
```

Run all tests with verbose output:
```bash
python tests/run_tests.py --setup-db -v
```

Run tests with coverage:
```bash
python tests/run_tests.py --setup-db -c
```

Run tests in parallel:
```bash
python tests/run_tests.py --setup-db -p
```

**Note:** The `--setup-db` flag is recommended for most test runs as it ensures a clean, isolated test environment.

### `--verbose-db` Flag

The `--verbose-db` flag controls the verbosity of database setup logs. By default, database setup shows minimal output:

- **Default (without `--verbose-db`)**: Shows only essential messages like "Setting up test database..." and "✅ Test database ready"
- **With `--verbose-db`**: Shows detailed step-by-step progress including table creation, trigger setup, and data insertion

Use `--verbose-db` when you need to debug database setup issues or want to see the full setup process.

**Examples:**
```bash
# Minimal database setup output (default)
python tests/run_tests.py --setup-db

# Verbose database setup output
python tests/run_tests.py --setup-db --verbose-db
```

### Running Specific Test Categories

Run only authentication tests:
```bash
python tests/run_tests.py --setup-db --auth-only
```

Run only portfolio tests:
```bash
python tests/run_tests.py --setup-db --portfolio-only
```

Run only admin tests:
```bash
python tests/run_tests.py --setup-db --admin-only
```

Run only API tests:
```bash
python tests/run_tests.py --setup-db --api-only
```

Run only logging tests:
```bash
python tests/run_tests.py --setup-db --logging-only
```

Run only integration tests:
```bash
python tests/run_tests.py --setup-db --integration-only
```

Run only validation tests:
```bash
python tests/run_tests.py --setup-db --validation-only
```

Run only error handling tests:
```bash
python tests/run_tests.py --setup-db --error-handling-only
```

### Running Specific Test Files

Run a specific test file:
```bash
python tests/run_tests.py --setup-db tests/unit/test_auth.py
```

Run tests in a specific directory:
```bash
python tests/run_tests.py --setup-db tests/unit/
```

### Running Tests with Docker Compose

When running the application with Docker Compose, you can run tests inside the container:

**Run all tests:**
```bash
docker-compose exec web python tests/run_tests.py --setup-db -v
```

**Run specific test categories:**
```bash
# API tests only
docker-compose exec web python tests/run_tests.py --setup-db --api-only -v

# Authentication tests only
docker-compose exec web python tests/run_tests.py --setup-db --auth-only -v
```

**Run tests with coverage:**
```bash
docker-compose exec web python tests/run_tests.py --setup-db -c -v
```

**Run tests in parallel:**
```bash
docker-compose exec web python tests/run_tests.py --setup-db -p -v
```

### Using pytest directly

You can also use pytest directly:
```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_auth.py

# Run specific test class
pytest tests/unit/test_auth.py::TestUserRegistration

# Run specific test method
pytest tests/unit/test_auth.py::TestUserRegistration::test_valid_user_registration
```

## Test Configuration

### Test Database Configuration

The test suite is configured to use a separate test database with the following characteristics:

- **Database Name**: `portfolioanalyzer_test`
- **Database User**: Root user (for full permissions)
- **Isolation**: Completely separate from production data
- **Clean State**: Dropped and recreated for each test run with `--setup-db`

**Environment Variables Used:**
- `DB_HOST`: Database host (default: localhost)
- `DB_ROOT_USER`: Root database user (default: root)
- `DB_ROOT_PASSWORD`: Root database password
- `TEST_DB_NAME`: Test database name (default: portfolioanalyzer_test)
- `DB_PORT`: Database port (default: 3306)

### Fixtures

The test suite uses several fixtures defined in `conftest.py`:

- `app`: Flask application instance for testing
- `client`: Test client for making HTTP requests
- `auth_headers`: Helper for creating authenticated requests
- `admin_headers`: Helper for creating admin authenticated requests
- `mock_db_connection`: Mock database connection
- `mock_yfinance`: Mock yfinance API
- `sample_*_data`: Sample data for testing

### Test Data

Test data is defined in `fixtures/test_data.py`:

- Sample users, portfolios, bonds, currencies, exchanges
- Invalid test data for negative testing
- Mock API responses
- SQL injection payloads
- XSS payloads
- Path traversal payloads

## Test Coverage

The test suite aims to achieve comprehensive coverage of:

- **Functional Testing**: All major features and workflows
- **Security Testing**: Authentication, authorization, input validation
- **Error Handling**: Database errors, API errors, network errors
- **Integration Testing**: End-to-end workflows
- **Performance Testing**: Basic performance and memory usage
- **Edge Cases**: Boundary conditions, invalid inputs

## Continuous Integration

The test suite is designed to be run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-xdist
    - name: Run tests
      run: python tests/run_tests.py --setup-db -c -p
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure the project root is in the Python path
2. **Database Permission Errors**: 
   - Use the `--setup-db` flag to ensure proper database setup
   - The test suite uses root database credentials for full permissions
   - If you see "SELECT command denied" errors, the test database setup needs to be run with root privileges
3. **Port Conflicts**: Tests use port 5000, make sure it's available
4. **File Permissions**: Ensure write permissions for log files
5. **Test Database Issues**:
   - If tests fail with database errors, try running with `--setup-db` to recreate the test database
   - The test database is automatically dropped and recreated when using `--setup-db`
   - Ensure your `.env` file has the correct `DB_ROOT_PASSWORD` set

### Database Permission Issues

If you encounter database permission errors like:
```
mysql.connector.errors.ProgrammingError: 1142 (42000): SELECT command denied to user 'portfolio_app'
```

**Solution**: Use the `--setup-db` flag which configures the test suite to use root database credentials:

```bash
python tests/run_tests.py --setup-db -v
```

This ensures the test database setup has full permissions to create tables, triggers, and procedures.

### Debug Mode

Run tests in debug mode:
```bash
pytest tests/ -v -s --pdb
```

This will drop into the debugger on test failures.

## Contributing

When adding new tests:

1. Follow the existing naming conventions
2. Use appropriate fixtures from `conftest.py`
3. Add test data to `fixtures/test_data.py` if needed
4. Update this README if adding new test categories
5. Ensure tests are isolated and don't depend on each other
6. Use descriptive test names and docstrings
7. Add both positive and negative test cases
