"""
Input validation tests for Portfolio Analyzer.
"""

import pytest
from tests.fixtures.test_data import SQL_INJECTION_PAYLOADS, XSS_PAYLOADS, PATH_TRAVERSAL_PAYLOADS


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
            assert response.status_code != 302
    
    def test_sql_injection_protection_in_login(self, client):
        """Test SQL injection protection in user login."""
        for payload in SQL_INJECTION_PAYLOADS:
            response = client.post('/auth/login', data={
                'username': payload,
                'userpwd': payload
            })
            
            # Should be rejected
            assert response.status_code != 302
    
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
            assert response.status_code != 302
    
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
            assert response.status_code != 302


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
            assert response.status_code != 302
    
    def test_xss_protection_in_login(self, client):
        """Test XSS protection in user login."""
        for payload in XSS_PAYLOADS:
            response = client.post('/auth/login', data={
                'username': payload,
                'userpwd': payload
            })
            
            # Should be rejected
            assert response.status_code != 302
    
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
            assert response.status_code != 302
    
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
            assert response.status_code != 302


class TestPathTraversalProtection:
    """Test path traversal protection."""
    
    def test_path_traversal_protection_in_log_viewer(self, client, admin_headers):
        """Test path traversal protection in log viewer."""
        headers = admin_headers()
        
        for payload in PATH_TRAVERSAL_PAYLOADS:
            response = client.get(f'/admin/logs/{payload}', headers=headers)
            
            # Should be denied access
            assert response.status_code in [403, 404]
    
    def test_path_traversal_protection_in_file_operations(self, client, admin_headers):
        """Test path traversal protection in file operations."""
        headers = admin_headers()
        
        for payload in PATH_TRAVERSAL_PAYLOADS:
            # Test in log file viewer
            response = client.get(f'/admin/logs/{payload}', headers=headers)
            
            # Should be denied access
            assert response.status_code in [403, 404]


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
        assert response.status_code != 302
    
    def test_portfolio_description_length_validation(self, client, auth_headers):
        """Test portfolio description length validation."""
        headers = auth_headers()
        
        # Too long
        response = client.post('/create_portfolio', data={
            'portfolioname': 'Test Portfolio',
            'portfoliodescription': 'a' * 10000,
            'currencycode': 'USD'
        }, headers=headers)
        assert response.status_code != 302


class TestInputFormatValidation:
    """Test input format validation."""
    
    def test_username_format_validation(self, client):
        """Test username format validation."""
        invalid_usernames = [
            'user@name',
            'user name',
            'user-name',
            'user.name',
            'user/name',
            'user\\name',
            'user:name',
            'user;name',
            'user,name',
            'user<name',
            'user>name',
            'user|name',
            'user?name',
            'user*name',
            'user"name',
            "user'name",
            'user`name',
            'user~name',
            'user!name',
            'user@name',
            'user#name',
            'user$name',
            'user%name',
            'user^name',
            'user&name',
            'user(name',
            'user)name',
            'user+name',
            'user=name',
            'user[name',
            'user]name',
            'user{name',
            'user}name',
            'user\tname',
            'user\nname',
            'user\rname'
        ]
        
        for username in invalid_usernames:
            response = client.post('/auth/register', data={
                'username': username,
                'userpwd': 'ValidPass123!',
                'confirm_password': 'ValidPass123!'
            })
            assert response.status_code != 302
    
    def test_currency_code_format_validation(self, client, admin_headers):
        """Test currency code format validation."""
        headers = admin_headers()
        
        invalid_currency_codes = [
            'INVALID123',
            'USD123',
            '123USD',
            'US',
            'USDD',
            'usd',
            'Usd',
            'uSd',
            'USD ',
            ' USD',
            'U SD',
            'U-S-D',
            'U.S.D',
            'U/S/D',
            'U\\S\\D',
            'U:S:D',
            'U;S;D',
            'U,S,D',
            'U<S>D',
            'U|S|D',
            'U?S?D',
            'U*S*D',
            'U"S"D',
            "U'S'D",
            'U`S`D',
            'U~S~D',
            'U!S!D',
            'U@S@D',
            'U#S#D',
            'U$S$D',
            'U%S%D',
            'U^S^D',
            'U&S&D',
            'U(S)D',
            'U+S+D',
            'U=S=D',
            'U[S]D',
            'U{S}D',
            'U\tS\tD',
            'U\nS\nD',
            'U\rS\rD'
        ]
        
        for currency_code in invalid_currency_codes:
            response = client.post('/admin/create_currency', data={
                'currencycode': currency_code,
                'currencyname': 'Test Currency'
            }, headers=headers)
            assert response.status_code != 302
    
    def test_exchange_symbol_format_validation(self, client, admin_headers):
        """Test exchange symbol format validation."""
        headers = admin_headers()
        
        invalid_exchange_symbols = [
            'INVALID123',
            'NYSE123',
            '123NYSE',
            'NY',
            'NYSES',
            'nyse',
            'Nyse',
            'nYse',
            'NYSE ',
            ' NYSE',
            'N YSE',
            'N-Y-S-E',
            'N.Y.S.E',
            'N/Y/S/E',
            'N\\Y\\S\\E',
            'N:Y:S:E',
            'N;Y;S;E',
            'N,Y,S,E',
            'N<Y>S>E',
            'N|Y|S|E',
            'N?Y?S?E',
            'N*Y*S*E',
            'N"Y"S"E',
            "N'Y'S'E",
            'N`Y`S`E',
            'N~Y~S~E',
            'N!Y!S!E',
            'N@Y@S@E',
            'N#Y#S#E',
            'N$Y$S$E',
            'N%Y%S%E',
            'N^Y^S^E',
            'N&Y&S&E',
            'N(Y)S(E)',
            'N+Y+S+E',
            'N=Y=S=E',
            'N[Y]S[E]',
            'N{Y}S{E}',
            'N\tY\tS\tE',
            'N\nY\nS\nE',
            'N\rY\rS\rE'
        ]
        
        for exchange_symbol in invalid_exchange_symbols:
            response = client.post('/admin/create_exchange', data={
                'exchangesymbol': exchange_symbol,
                'exchangename': 'Test Exchange',
                'regionid': 1
            }, headers=headers)
            assert response.status_code != 302


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
        assert response.status_code != 302
        
        # Missing currency code
        response = client.post('/create_portfolio', data={
            'portfolioname': 'Test Portfolio',
            'portfoliodescription': 'A test portfolio'
        }, headers=headers)
        assert response.status_code != 302
    
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
        assert response.status_code != 302
        
        # Missing bond symbol
        response = client.post('/admin/create_security', data={
            'bondname': 'Test Security',
            'bondcategoryid': 1,
            'bondcurrencyid': 1,
            'bondsector': 'Technology',
            'exchangeid': 1
        }, headers=headers)
        assert response.status_code != 302


class TestDataTypeValidation:
    """Test data type validation."""
    
    def test_numeric_field_validation(self, client, auth_headers):
        """Test numeric field validation."""
        headers = auth_headers()
        
        # Invalid numeric values
        invalid_numeric_values = [
            'not_a_number',
            '12.34.56',
            '12,34',
            '12 34',
            '12-34',
            '12/34',
            '12\\34',
            '12:34',
            '12;34',
            '12<34',
            '12>34',
            '12|34',
            '12?34',
            '12*34',
            '12"34',
            "12'34",
            '12`34',
            '12~34',
            '12!34',
            '12@34',
            '12#34',
            '12$34',
            '12%34',
            '12^34',
            '12&34',
            '12(34',
            '12)34',
            '12+34',
            '12=34',
            '12[34',
            '12]34',
            '12{34',
            '12}34',
            '12\t34',
            '12\n34',
            '12\r34'
        ]
        
        for invalid_value in invalid_numeric_values:
            response = client.post('/create_portfolio', data={
                'portfolioname': 'Test Portfolio',
                'portfoliodescription': 'A test portfolio',
                'currencycode': 'USD',
                'quantity': invalid_value
            }, headers=headers)
            assert response.status_code != 302
    
    def test_boolean_field_validation(self, client, admin_headers):
        """Test boolean field validation."""
        headers = admin_headers()
        
        # Invalid boolean values
        invalid_boolean_values = [
            'not_a_boolean',
            'true',
            'false',
            '1',
            '0',
            'yes',
            'no',
            'on',
            'off',
            'enabled',
            'disabled',
            'active',
            'inactive'
        ]
        
        for invalid_value in invalid_boolean_values:
            response = client.post('/admin/create_user', data={
                'username': 'testuser',
                'userpwd': 'ValidPass123!',
                'is_admin': invalid_value
            }, headers=headers)
            assert response.status_code != 302


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
        assert response.status_code == 302  # Should be valid
        
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
        assert response.status_code == 302  # Should be valid
        
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
        assert response.status_code == 302  # Should be valid
        
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
        assert response.status_code == 302  # Should be valid
        
        # Just above maximum length
        response = client.post('/auth/register', data={
            'username': 'boundarytest4',
            'userpwd': 'ValidPass123!' + 'a' * 1000,  # Above maximum length
            'confirm_password': 'ValidPass123!' + 'a' * 1000
        })
        assert response.status_code != 302  # Should be invalid
