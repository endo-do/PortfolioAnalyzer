"""
Test data fixtures for Portfolio Analyzer tests.
"""

import os
from datetime import datetime, timedelta

# Sample test data for various test scenarios

SAMPLE_USERS = [
    {
        'username': 'testuser1',
        'userpwd': 'TestPass123!',
        'is_admin': False
    },
    {
        'username': 'testuser2',
        'userpwd': 'AnotherPass456!',
        'is_admin': False
    },
    {
        'username': 'admin',
        'userpwd': 'AdminPass123!',
        'is_admin': True
    }
]

SAMPLE_PORTFOLIOS = [
    {
        'portfolioname': 'Growth Portfolio',
        'portfoliodescription': 'High growth potential investments',
        'currencycode': 'USD'
    },
    {
        'portfolioname': 'Conservative Portfolio',
        'portfoliodescription': 'Low risk, stable returns',
        'currencycode': 'EUR'
    },
    {
        'portfolioname': 'Tech Portfolio',
        'portfoliodescription': 'Technology sector focus',
        'currencycode': 'USD'
    }
]

SAMPLE_BONDS = [
    {
        'bondname': 'Apple Inc. Bond',
        'bondsymbol': 'AAPL',
        'bondcategoryid': 1,
        'bondcurrencyid': 1,
        'bondsector': 'Technology',
        'exchangeid': 1
    },
    {
        'bondname': 'Microsoft Corp Bond',
        'bondsymbol': 'MSFT',
        'bondcategoryid': 1,
        'bondcurrencyid': 1,
        'bondsector': 'Technology',
        'exchangeid': 1
    },
    {
        'bondname': 'Tesla Inc Bond',
        'bondsymbol': 'TSLA',
        'bondcategoryid': 2,
        'bondcurrencyid': 1,
        'bondsector': 'Automotive',
        'exchangeid': 1
    }
]

SAMPLE_CURRENCIES = [
    {
        'currencycode': 'USD',
        'currencyname': 'US Dollar'
    },
    {
        'currencycode': 'EUR',
        'currencyname': 'Euro'
    },
    {
        'currencycode': 'GBP',
        'currencyname': 'British Pound'
    },
    {
        'currencycode': 'JPY',
        'currencyname': 'Japanese Yen'
    }
]

SAMPLE_EXCHANGES = [
    {
        'exchangename': 'NYSE',
        'exchangename': 'New York Stock Exchange',
        'regionid': 1
    },
    {
        'exchangename': 'NASDAQ',
        'exchangename': 'NASDAQ Stock Market',
        'regionid': 1
    },
    {
        'exchangename': 'LSE',
        'exchangename': 'London Stock Exchange',
        'regionid': 2
    }
]

SAMPLE_REGIONS = [
    {
        'regionname': 'North America'
    },
    {
        'regionname': 'Europe'
    },
    {
        'regionname': 'Asia'
    }
]

SAMPLE_SECTORS = [
    {
        'sectorname': 'Technology'
    },
    {
        'sectorname': 'Healthcare'
    },
    {
        'sectorname': 'Finance'
    },
    {
        'sectorname': 'Energy'
    }
]

SAMPLE_BOND_CATEGORIES = [
    {
        'bondcategoryname': 'Corporate Bonds'
    },
    {
        'bondcategoryname': 'Government Bonds'
    },
    {
        'bondcategoryname': 'Municipal Bonds'
    }
]

# Invalid test data for negative testing
INVALID_PASSWORDS = [
    '123',  # Too short
    'password',  # Too common
    '12345678',  # No special characters
    'Password',  # No numbers
    'PASSWORD123',  # No lowercase
    'password123',  # No uppercase
    'Test123',  # No special characters
    '',  # Empty
    'a' * 100,  # Too long
]

INVALID_USERNAMES = [
    '',  # Empty
    'a',  # Too short
    'a' * 100,  # Too long
    'user@name',  # Invalid characters
    'user name',  # Spaces
    'user-name',  # Hyphens
]

INVALID_PORTFOLIO_NAMES = [
    '',  # Empty
    'a' * 1000,  # Too long
    '   ',  # Only spaces
]

# Mock API responses
MOCK_YFINANCE_RESPONSE = {
    'AAPL': {
        'currentPrice': 150.25,
        'previousClose': 148.50,
        'change': 1.75,
        'changePercent': 1.18
    },
    'MSFT': {
        'currentPrice': 300.45,
        'previousClose': 298.20,
        'change': 2.25,
        'changePercent': 0.75
    }
}

MOCK_EXCHANGE_RATES = {
    'USD_EUR': 0.85,
    'USD_GBP': 0.73,
    'USD_JPY': 110.50,
    'EUR_USD': 1.18,
    'GBP_USD': 1.37,
    'JPY_USD': 0.009
}

# Test log entries
SAMPLE_LOG_ENTRIES = [
    {
        'timestamp': datetime.now() - timedelta(hours=1),
        'level': 'INFO',
        'message': 'User logged in successfully',
        'user_id': 1
    },
    {
        'timestamp': datetime.now() - timedelta(minutes=30),
        'level': 'WARNING',
        'message': 'Failed login attempt',
        'user_id': None
    },
    {
        'timestamp': datetime.now() - timedelta(minutes=15),
        'level': 'ERROR',
        'message': 'Database connection failed',
        'user_id': None
    }
]

# SQL injection test cases
SQL_INJECTION_PAYLOADS = [
    "'; DROP TABLE users; --",
    "' OR '1'='1",
    "'; INSERT INTO users (username, userpwd) VALUES ('hacker', 'password'); --",
    "' UNION SELECT * FROM users --",
    "'; UPDATE users SET userpwd='hacked' WHERE username='admin'; --"
]

# XSS test cases
XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "javascript:alert('XSS')",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "';alert('XSS');//"
]

# File path traversal test cases
PATH_TRAVERSAL_PAYLOADS = [
    "../../../etc/passwd",
    "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
    "....//....//....//etc/passwd",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
]
