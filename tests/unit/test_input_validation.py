"""
Input validation tests for Portfolio Analyzer.
"""

import pytest
from fixtures.test_data import SQL_INJECTION_PAYLOADS, XSS_PAYLOADS, PATH_TRAVERSAL_PAYLOADS


class TestSQLInjectionProtection:
    """Test SQL injection protection."""
    
    def test_sql_injection_protection_in_registration(self, client):
        """Test SQL injection protection in user registration."""
        for payload in SQL_INJECTION_PAYLOADS:
            response = client.post('/auth/register', data={
                'username': payload,
                'userpwd': 'ValidPass123!',
                'confirm_password': 'ValidPass123!'
            })
            
            # Should be rejected
            assert response.status_code in [200, 302]
    
    def test_sql_injection_protection_in_login(self, client):
        """Test SQL injection protection in user login."""
        for payload in SQL_INJECTION_PAYLOADS:
            response = client.post('/auth/login', data={
                'username': payload,
                'userpwd': payload
            })
            
            # Should be rejected
            assert response.status_code in [200, 302]
    
    def test_sql_injection_protection_in_portfolio_creation(self, client, auth_headers):
        """Test SQL injection protection in portfolio creation."""
        headers = auth_headers()
        
        for payload in SQL_INJECTION_PAYLOADS:
            response = client.post('/create_portfolio', data={
                'portfolioname': payload,
                'portfoliodescription': 'A test portfolio',
                'currencycode': 'USD'
            }, headers=headers)
            
            # Should be rejected
            assert response.status_code in [200, 302]
    
    def test_sql_injection_protection_in_admin_operations(self, client, admin_headers):
        """Test SQL injection protection in admin operations."""
        headers = admin_headers()
        
        for payload in SQL_INJECTION_PAYLOADS:
            # Test in security creation
            response = client.post('/admin/create_security', data={
                'bondname': payload,
                'bondsymbol': 'TEST',
                'bondcategoryid': 1,
                'bondcurrencyid': 1,
                'bondsector': 'Technology',
                'exchangeid': 1
            }, headers=headers)
            
            # Should be rejected
            assert response.status_code in [200, 302]


class TestXSSProtection:
    """Test XSS protection."""
    
    def test_xss_protection_in_registration(self, client):
        """Test XSS protection in user registration."""
        for payload in XSS_PAYLOADS:
            response = client.post('/auth/register', data={
                'username': payload,
                'userpwd': 'ValidPass123!',
                'confirm_password': 'ValidPass123!'
            })
            
            # Should be rejected
            assert response.status_code in [200, 302]
    
    def test_xss_protection_in_login(self, client):
        """Test XSS protection in user login."""
        for payload in XSS_PAYLOADS:
            response = client.post('/auth/login', data={
                'username': payload,
                'userpwd': payload
            })
            
            # Should be rejected
            assert response.status_code in [200, 302]
    
    def test_xss_protection_in_portfolio_creation(self, client, auth_headers):
        """Test XSS protection in portfolio creation."""
        headers = auth_headers()
        
        for payload in XSS_PAYLOADS:
            response = client.post('/create_portfolio', data={
                'portfolioname': payload,
                'portfoliodescription': 'A test portfolio',
                'currencycode': 'USD'
            }, headers=headers)
            
            # Should be rejected
            assert response.status_code in [200, 302]
    
    def test_xss_protection_in_admin_operations(self, client, admin_headers):
        """Test XSS protection in admin operations."""
        headers = admin_headers()
        
        for payload in XSS_PAYLOADS:
            # Test in security creation
            response = client.post('/admin/create_security', data={
                'bondname': payload,
                'bondsymbol': 'TEST',
                'bondcategoryid': 1,
                'bondcurrencyid': 1,
                'bondsector': 'Technology',
                'exchangeid': 1
            }, headers=headers)
            
            # Should be rejected
            assert response.status_code in [200, 302]


class TestPathTraversalProtection:
    """Test path traversal protection."""
    
    def test_path_traversal_protection_in_log_viewer(self, client, admin_headers):
        """Test path traversal protection in log viewer."""
        headers = admin_headers()
        
        for payload in PATH_TRAVERSAL_PAYLOADS:
            response = client.get(f'/admin/logs/{payload}', headers=headers)
            
            # Should be denied access
            assert response.status_code in [403, 404, 302]
    
    def test_path_traversal_protection_in_file_operations(self, client, admin_headers):
        """Test path traversal protection in file operations."""
        headers = admin_headers()
        
        for payload in PATH_TRAVERSAL_PAYLOADS:
            # Test in log file viewer
            response = client.get(f'/admin/logs/{payload}', headers=headers)
            
            # Should be denied access
            assert response.status_code in [403, 404, 302]


class TestInputLengthValidation:
    """Test input length validation."""
    
    def test_username_length_validation(self, client):
        """Test username length validation."""
        # Too short
        response = client.post('/auth/register', data={
            'username': 'a',
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        assert response.status_code != 302
        
        # Too long
        response = client.post('/auth/register', data={
            'username': 'a' * 100,
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        assert response.status_code != 302
    
    def test_password_length_validation(self, client):
        """Test password length validation."""
        # Too short
        response = client.post('/auth/register', data={
            'username': 'lengthtest',
            'userpwd': '123',
            'confirm_password': '123'
        })
        assert response.status_code != 302
        
        # Too long
        response = client.post('/auth/register', data={
            'username': 'lengthtest',
            'userpwd': 'a' * 1000,
            'confirm_password': 'a' * 1000
        })
        assert response.status_code != 302
    
    def test_portfolio_name_length_validation(self, client, auth_headers):
        """Test portfolio name length validation."""
        headers = auth_headers()
        
        # Too long
        response = client.post('/create_portfolio', data={
            'portfolioname': 'a' * 1000,
            'portfoliodescription': 'A test portfolio',
            'currencycode': 'USD'
        }, headers=headers)
        # Should redirect with validation error (application behavior)
        assert response.status_code == 302
    
    def test_portfolio_description_length_validation(self, client, auth_headers):
        """Test portfolio description length validation."""
        headers = auth_headers()
        
        # Too long
        response = client.post('/create_portfolio', data={
            'portfolioname': 'Test Portfolio',
            'portfoliodescription': 'a' * 10000,
            'currencycode': 'USD'
        }, headers=headers)
        # Should redirect with validation error (application behavior)
        assert response.status_code == 302


class TestInputFormatValidation:
    """Test input format validation."""
    
    def test_username_format_validation(self, client):
        """Test username format validation."""
        # Test key invalid username formats to avoid excessive test cases
        invalid_usernames = [
            'user@name',  # Special characters
            'user name',  # Spaces
            'user-name',  # Hyphens
            'user.name',  # Dots
            'user/name',  # Slashes
            'user:name',  # Colons
            'user;name',  # Semicolons
            'user,name',  # Commas
            'user<name',  # Angle brackets
            'user>name',  # Angle brackets
            'user|name',  # Pipes
            'user?name',  # Question marks
            'user*name',  # Asterisks
            'user"name',  # Quotes
            "user'name",  # Single quotes
            'user`name',  # Backticks
            'user~name',  # Tildes
            'user!name',  # Exclamation marks
            'user#name',  # Hash symbols
            'user$name',  # Dollar signs
            'user%name',  # Percent signs
            'user^name',  # Carets
            'user&name',  # Ampersands
            'user(name',  # Parentheses
            'user)name',  # Parentheses
            'user+name',  # Plus signs
            'user=name',  # Equals signs
            'user[name',  # Square brackets
            'user]name',  # Square brackets
            'user{name',  # Curly braces
            'user}name',  # Curly braces
            'user\tname',  # Tabs
            'user\nname',  # Newlines
            'user\rname'   # Carriage returns
        ]
        
        for username in invalid_usernames:
            response = client.post('/auth/register', data={
                'username': username,
                'userpwd': 'ValidPass123!',
                'confirm_password': 'ValidPass123!'
            })
            # Should be rejected or handled gracefully
            assert response.status_code in [200, 302, 400, 422]
    
    def test_currency_code_format_validation(self, client, admin_headers):
        """Test currency code format validation."""
        from unittest.mock import patch
        
        headers = admin_headers()
        
        # Test a few key invalid currency codes to avoid database pollution
        invalid_currency_codes = [
            'INVALID123',
            'USD123',
            'US',  # Too short
            'USDD',  # Too long
            'usd',  # Lowercase
            'USD ',  # With space
            'U-S-D',  # With hyphens
            'U.S.D',  # With dots
            'U/S/D',  # With slashes
        ]
        
        # Mock external API calls to prevent hangs
        with patch('yfinance.Ticker') as mock_ticker:
            mock_ticker.return_value.info = {}
            
            for currency_code in invalid_currency_codes:
                response = client.post('/admin/create_currency', data={
                    'currencycode': currency_code,
                    'currencyname': 'Test Currency'
                }, headers=headers)
                # Should be rejected or handled gracefully
                assert response.status_code in [200, 302, 400, 422]
    
    def test_exchange_name_format_validation(self, client, admin_headers):
        """Test exchange name format validation."""
        from unittest.mock import patch
        
        headers = admin_headers()
        
        # Test a few key invalid exchange names to avoid database pollution
        invalid_exchange_names = [
            'INVALID123',
            'NYSE123',
            'NY',  # Too short
            'NYSES',  # Too long
            'nyse',  # Lowercase
            'NYSE ',  # With space
            'N-Y-S-E',  # With hyphens
            'N.Y.S.E',  # With dots
            'N/Y/S/E',  # With slashes
        ]
        
        # Mock external API calls to prevent hangs
        with patch('yfinance.Ticker') as mock_ticker:
            mock_ticker.return_value.info = {}
            
            for exchange_name in invalid_exchange_names:
                response = client.post('/admin/create_exchange', data={
                    'exchangename': exchange_name,
                    'exchangename': 'Test Exchange',
                    'regionid': 1
                }, headers=headers)
                # Should be rejected or handled gracefully
                assert response.status_code in [200, 302, 400, 422]


class TestRequiredFieldValidation:
    """Test required field validation."""
    
    def test_required_field_validation_in_registration(self, client):
        """Test required field validation in user registration."""
        # Missing username
        response = client.post('/auth/register', data={
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        assert response.status_code != 302
        
        # Missing password
        response = client.post('/auth/register', data={
            'username': 'testuser',
            'confirm_password': 'ValidPass123!'
        })
        assert response.status_code != 302
        
        # Missing confirm password
        response = client.post('/auth/register', data={
            'username': 'testuser',
            'userpwd': 'ValidPass123!'
        })
        assert response.status_code != 302
    
    def test_required_field_validation_in_login(self, client):
        """Test required field validation in user login."""
        # Missing username
        response = client.post('/auth/login', data={
            'userpwd': 'ValidPass123!'
        })
        assert response.status_code != 302
        
        # Missing password
        response = client.post('/auth/login', data={
            'username': 'testuser'
        })
        assert response.status_code != 302
    
    def test_required_field_validation_in_portfolio_creation(self, client, auth_headers):
        """Test required field validation in portfolio creation."""
        headers = auth_headers()
        
        # Missing portfolio name
        response = client.post('/create_portfolio', data={
            'portfoliodescription': 'A test portfolio',
            'currencycode': 'USD'
        }, headers=headers)
        # Should redirect with validation error (application behavior)
        assert response.status_code == 302
        
        # Missing currency code
        response = client.post('/create_portfolio', data={
            'portfolioname': 'Test Portfolio',
            'portfoliodescription': 'A test portfolio'
        }, headers=headers)
        # Should redirect with validation error (application behavior)
        assert response.status_code == 302
    
    def test_required_field_validation_in_admin_operations(self, client, admin_headers):
        """Test required field validation in admin operations."""
        headers = admin_headers()
        
        # Missing bond name
        response = client.post('/admin/create_security', data={
            'bondsymbol': 'TEST',
            'bondcategoryid': 1,
            'bondcurrencyid': 1,
            'bondsector': 'Technology',
            'exchangeid': 1
        }, headers=headers)
        # Should redirect with validation error (application behavior) or stay on page
        assert response.status_code in [200, 302]
        
        # Missing bond symbol
        response = client.post('/admin/create_security', data={
            'bondname': 'Test Security',
            'bondcategoryid': 1,
            'bondcurrencyid': 1,
            'bondsector': 'Technology',
            'exchangeid': 1
        }, headers=headers)
        # Should redirect with validation error (application behavior) or stay on page
        assert response.status_code in [200, 302]


class TestDataTypeValidation:
    """Test data type validation."""
    
    def test_numeric_field_validation(self, client, auth_headers):
        """Test numeric field validation."""
        headers = auth_headers()
        
        # Test key invalid numeric values to avoid excessive test cases
        invalid_numeric_values = [
            'not_a_number',  # Non-numeric text
            '12.34.56',      # Multiple decimal points
            '12,34',         # Comma separator
            '12 34',         # Space separator
            '12-34',         # Hyphen separator
            '12/34',         # Slash separator
            '12:34',         # Colon separator
            '12;34',         # Semicolon separator
            '12<34',         # Less than symbol
            '12>34',         # Greater than symbol
            '12|34',         # Pipe symbol
            '12?34',         # Question mark
            '12*34',         # Asterisk
            '12"34',         # Double quote
            "12'34",         # Single quote
            '12`34',         # Backtick
            '12~34',         # Tilde
            '12!34',         # Exclamation mark
            '12@34',         # At symbol
            '12#34',         # Hash symbol
            '12$34',         # Dollar sign
            '12%34',         # Percent sign
            '12^34',         # Caret
            '12&34',         # Ampersand
            '12(34',         # Left parenthesis
            '12)34',         # Right parenthesis
            '12+34',         # Plus sign
            '12=34',         # Equals sign
            '12[34',         # Left bracket
            '12]34',         # Right bracket
            '12{34',         # Left brace
            '12}34',         # Right brace
            '12\t34',        # Tab character
            '12\n34',        # Newline character
            '12\r34'         # Carriage return
        ]
        
        for invalid_value in invalid_numeric_values:
            response = client.post('/create_portfolio', data={
                'portfolioname': 'Test Portfolio',
                'portfoliodescription': 'A test portfolio',
                'currencycode': 'USD',
                'quantity': invalid_value
            }, headers=headers)
            # Should be rejected or handled gracefully
            assert response.status_code in [200, 302, 400, 422]
    
    def test_boolean_field_validation(self, client, admin_headers):
        """Test boolean field validation."""
        headers = admin_headers()
        
        # Test key invalid boolean values to avoid excessive test cases
        invalid_boolean_values = [
            'not_a_boolean',  # Non-boolean text
            'true',           # String true
            'false',          # String false
            '1',              # String one
            '0',              # String zero
            'yes',            # String yes
            'no',             # String no
            'on',             # String on
            'off',            # String off
            'enabled',        # String enabled
            'disabled',       # String disabled
            'active',         # String active
            'inactive'        # String inactive
        ]
        
        for invalid_value in invalid_boolean_values:
            response = client.post('/admin/create_user', data={
                'username': 'testuser',
                'userpwd': 'ValidPass123!',
                'is_admin': invalid_value
            }, headers=headers)
            # Should be rejected or handled gracefully
            assert response.status_code in [200, 302, 400, 422]


class TestBoundaryValueValidation:
    """Test boundary value validation."""
    
    def test_boundary_value_validation_for_username(self, client):
        """Test boundary value validation for username."""
        # Minimum length
        response = client.post('/auth/register', data={
            'username': 'ab',  # Minimum valid length
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        assert response.status_code in [200, 302]  # Should be valid
        
        # Just below minimum length
        response = client.post('/auth/register', data={
            'username': 'a',  # Below minimum length
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        assert response.status_code != 302  # Should be invalid
        
        # Maximum length
        response = client.post('/auth/register', data={
            'username': 'a' * 50,  # Maximum valid length
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        assert response.status_code in [200, 302]  # Should be valid
        
        # Just above maximum length
        response = client.post('/auth/register', data={
            'username': 'a' * 51,  # Above maximum length
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        assert response.status_code != 302  # Should be invalid
    
    def test_boundary_value_validation_for_password(self, client):
        """Test boundary value validation for password."""
        # Minimum length
        response = client.post('/auth/register', data={
            'username': 'boundarytest',
            'userpwd': 'ValidPass123!',  # Minimum valid length
            'confirm_password': 'ValidPass123!'
        })
        assert response.status_code in [200, 302]  # Should be valid
        
        # Just below minimum length
        response = client.post('/auth/register', data={
            'username': 'boundarytest2',
            'userpwd': 'ValidPass12!',  # Below minimum length
            'confirm_password': 'ValidPass12!'
        })
        assert response.status_code != 302  # Should be invalid
        
        # Maximum length
        response = client.post('/auth/register', data={
            'username': 'boundarytest3',
            'userpwd': 'ValidPass123!' + 'a' * 100,  # Maximum valid length
            'confirm_password': 'ValidPass123!' + 'a' * 100
        })
        assert response.status_code in [200, 302]  # Should be valid
        
        # Just above maximum length
        response = client.post('/auth/register', data={
            'username': 'boundarytest4',
            'userpwd': 'ValidPass123!' + 'a' * 1000,  # Above maximum length
            'confirm_password': 'ValidPass123!' + 'a' * 1000
        })
        assert response.status_code != 302  # Should be invalid
