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

### Basic Test Execution

Run all tests:
```bash
python tests/run_tests.py
```

Run tests with verbose output:
```bash
python tests/run_tests.py -v
```

Run tests with coverage:
```bash
python tests/run_tests.py -c
```

Run tests in parallel:
```bash
python tests/run_tests.py -p
```

### Running Specific Test Categories

Run only authentication tests:
```bash
python tests/run_tests.py --auth-only
```

Run only portfolio tests:
```bash
python tests/run_tests.py --portfolio-only
```

Run only admin tests:
```bash
python tests/run_tests.py --admin-only
```

Run only API tests:
```bash
python tests/run_tests.py --api-only
```

Run only logging tests:
```bash
python tests/run_tests.py --logging-only
```

Run only integration tests:
```bash
python tests/run_tests.py --integration-only
```

Run only validation tests:
```bash
python tests/run_tests.py --validation-only
```

Run only error handling tests:
```bash
python tests/run_tests.py --error-handling-only
```

### Running Specific Test Files

Run a specific test file:
```bash
python tests/run_tests.py tests/unit/test_auth.py
```

Run tests in a specific directory:
```bash
python tests/run_tests.py tests/unit/
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
      run: python tests/run_tests.py -c -p
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure the project root is in the Python path
2. **Database Errors**: Tests use a temporary database, ensure proper cleanup
3. **Port Conflicts**: Tests use port 5000, make sure it's available
4. **File Permissions**: Ensure write permissions for log files

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
