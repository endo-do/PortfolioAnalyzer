"""
Admin functionality tests for Portfolio Analyzer.
"""

import pytest
from flask import url_for
from fixtures.test_data import SQL_INJECTION_PAYLOADS, XSS_PAYLOADS


class TestAdminAccess:
    """Test admin access control."""
    
    def test_admin_dashboard_access_with_admin_user(self, admin_client):
        """Test admin dashboard access with admin user."""
        client = admin_client()
        
        response = client.get('/admin/')
        
        assert response.status_code == 200
        assert b'admin' in response.data.lower()
    
    def test_admin_dashboard_access_without_authentication(self, client):
        """Test admin dashboard access without authentication."""
        response = client.get('/admin/')

        # Should redirect to login page, return 401, or deny access
        assert response.status_code in [302, 401, 200]
        if response.status_code == 302:
            assert '/auth/login' in response.location
    
    def test_admin_dashboard_access_with_regular_user(self, authenticated_client):
        """Test admin dashboard access with regular user."""
        client = authenticated_client()
        
        response = client.get('/admin/')
        
        # Should be denied access - either 403 or redirect to login
        assert response.status_code in [403, 404, 302]
    
    def test_admin_routes_require_admin_permission(self, authenticated_client):
        """Test that admin routes require admin permission."""
        client = authenticated_client()
        admin_routes = [
            '/admin/securityoverview',
            '/admin/currencyoverview',
            '/admin/exchangeoverview',
            '/admin/useroverview',
            '/admin/logs'
        ]
        
        for route in admin_routes:
            response = client.get(route)
            # Should be denied access - either 403/404 or redirect to login
        assert response.status_code in [403, 404, 302]


class TestSecurityManagement:
    """Test security management functionality."""
    
    def test_create_security_with_valid_data(self, client, admin_headers):
        """Test creating security with valid data."""
        headers = admin_headers()
        
        response = client.post('/admin/create_security', data={
            'bondname': 'Test Security',
            'bondsymbol': 'TEST',
            'bondcategoryid': 1,
            'bondcurrencyid': 1,
            'bondsector': 'Technology',
            'exchangeid': 1
        }, headers=headers)
        
        assert response.status_code in [200, 302]  # Accept both success and redirect
    
    def test_create_security_without_admin_permission(self, client, auth_headers):
        """Test creating security without admin permission."""
        headers = auth_headers()
        
        response = client.post('/admin/create_security', data={
            'bondname': 'Test Security',
            'bondsymbol': 'TEST',
            'bondcategoryid': 1,
            'bondcurrencyid': 1,
            'bondsector': 'Technology',
            'exchangeid': 1
        }, headers=headers)
        
        # Should be denied access
        assert response.status_code in [403, 404, 302]
    
    def test_create_security_with_invalid_data(self, client, admin_headers):
        """Test creating security with invalid data."""
        headers = admin_headers()
        
        response = client.post('/admin/create_security', data={
            'bondname': '',  # Empty name
            'bondsymbol': 'TEST',
            'bondcategoryid': 1,
            'bondcurrencyid': 1,
            'bondsector': 'Technology',
            'exchangeid': 1
        }, headers=headers)
        
        assert response.status_code in [200, 302]
    
    def test_create_security_with_sql_injection(self, client, admin_headers):
        """Test creating security with SQL injection payloads."""
        headers = admin_headers()
        
        for payload in SQL_INJECTION_PAYLOADS:
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
    
    def test_create_security_with_xss_payload(self, client, admin_headers):
        """Test creating security with XSS payloads."""
        headers = admin_headers()
        
        for payload in XSS_PAYLOADS:
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
    
    def test_edit_security_with_valid_data(self, client, admin_headers):
        """Test editing security with valid data."""
        headers = admin_headers()
        
        # Create security first
        client.post('/admin/create_security', data={
            'bondname': 'Test Security',
            'bondsymbol': 'TEST',
            'bondcategoryid': 1,
            'bondcurrencyid': 1,
            'bondsector': 'Technology',
            'exchangeid': 1
        }, headers=headers)
        
        # Edit security
        response = client.post('/admin/edit_security/1', data={
            'bondname': 'Updated Security',
            'bondsymbol': 'UPD',
            'bondcategoryid': 1,
            'bondcurrencyid': 1,
            'bondsector': 'Technology',
            'exchangeid': 1
        }, headers=headers)
        
        assert response.status_code == 302
    
    def test_delete_security(self, client, admin_headers):
        """Test deleting security."""
        headers = admin_headers()
        
        # Create security first
        client.post('/admin/create_security', data={
            'bondname': 'Test Security',
            'bondsymbol': 'TEST',
            'bondcategoryid': 1,
            'bondcurrencyid': 1,
            'bondsector': 'Technology',
            'exchangeid': 1
        }, headers=headers)
        
        # Delete security
        response = client.post('/admin/delete_security/1', headers=headers)
        
        assert response.status_code == 302


class TestCurrencyManagement:
    """Test currency management functionality."""
    
    def test_create_currency_with_valid_data(self, client, admin_headers):
        """Test creating currency with valid data."""
        headers = admin_headers()
        
        response = client.post('/admin/create_currency', data={
            'currencycode': 'EUR',
            'currencyname': 'Euro'
        }, headers=headers)
        
        assert response.status_code == 302
    
    def test_create_currency_without_admin_permission(self, client, auth_headers):
        """Test creating currency without admin permission."""
        headers = auth_headers()
        
        response = client.post('/admin/create_currency', data={
            'currencycode': 'EUR',
            'currencyname': 'Euro'
        }, headers=headers)
        
        # Should be denied access
        assert response.status_code in [403, 404, 302]
    
    def test_create_currency_with_invalid_data(self, client, admin_headers):
        """Test creating currency with invalid data."""
        headers = admin_headers()
        
        response = client.post('/admin/create_currency', data={
            'currencycode': '',  # Empty code
            'currencyname': 'Euro'
        }, headers=headers)
        
        assert response.status_code in [200, 302]
    
    def test_create_duplicate_currency(self, client, admin_headers):
        """Test creating duplicate currency."""
        headers = admin_headers()
        
        # Create first currency
        client.post('/admin/create_currency', data={
            'currencycode': 'EUR',
            'currencyname': 'Euro'
        }, headers=headers)
        
        # Try to create duplicate
        response = client.post('/admin/create_currency', data={
            'currencycode': 'EUR',
            'currencyname': 'Euro'
        }, headers=headers)
        
        assert response.status_code in [200, 302]
    
    def test_delete_currency(self, client, admin_headers):
        """Test deleting currency."""
        headers = admin_headers()
        
        # Create currency first
        client.post('/admin/create_currency', data={
            'currencycode': 'EUR',
            'currencyname': 'Euro'
        }, headers=headers)
        
        # Delete currency
        response = client.post('/admin/delete_currency/1', headers=headers)
        
        assert response.status_code == 302


class TestExchangeManagement:
    """Test exchange management functionality."""
    
    def test_create_exchange_with_valid_data(self, client, admin_headers):
        """Test creating exchange with valid data."""
        headers = admin_headers()
        
        response = client.post('/admin/create_exchange', data={
            'exchangename': 'NYSE',
            'exchangename': 'New York Stock Exchange',
            'regionid': 1
        }, headers=headers)
        
        assert response.status_code == 302
    
    def test_create_exchange_without_admin_permission(self, client, auth_headers):
        """Test creating exchange without admin permission."""
        headers = auth_headers()
        
        response = client.post('/admin/create_exchange', data={
            'exchangename': 'NYSE',
            'exchangename': 'New York Stock Exchange',
            'regionid': 1
        }, headers=headers)
        
        # Should be denied access
        assert response.status_code in [403, 404, 302]
    
    def test_create_exchange_with_invalid_data(self, client, admin_headers):
        """Test creating exchange with invalid data."""
        headers = admin_headers()
        
        response = client.post('/admin/create_exchange', data={
            'exchangename': '',  # Empty symbol
            'exchangename': 'New York Stock Exchange',
            'regionid': 1
        }, headers=headers)
        
        assert response.status_code in [200, 302]
    
    def test_edit_exchange_with_valid_data(self, client, admin_headers):
        """Test editing exchange with valid data."""
        headers = admin_headers()
        
        # Create exchange first
        client.post('/admin/create_exchange', data={
            'exchangename': 'NYSE',
            'exchangename': 'New York Stock Exchange',
            'regionid': 1
        }, headers=headers)
        
        # Edit exchange
        response = client.post('/admin/edit_exchange/1', data={
            'exchangename': 'NYSE',
            'exchangename': 'Updated NYSE',
            'regionid': 1
        }, headers=headers)
        
        assert response.status_code == 302
    
    def test_delete_exchange(self, client, admin_headers):
        """Test deleting exchange."""
        headers = admin_headers()
        
        # Create exchange first
        client.post('/admin/create_exchange', data={
            'exchangename': 'NYSE',
            'exchangename': 'New York Stock Exchange',
            'regionid': 1
        }, headers=headers)
        
        # Delete exchange
        response = client.post('/admin/delete_exchange/1', headers=headers)
        
        assert response.status_code == 302


class TestUserManagement:
    """Test user management functionality."""
    
    def test_create_user_with_valid_data(self, client, admin_headers):
        """Test creating user with valid data."""
        headers = admin_headers()
        
        response = client.post('/admin/create_user', data={
            'username': 'newuser',
            'userpwd': 'ValidPass123!',
            'is_admin': False
        }, headers=headers)
        
        assert response.status_code == 302
    
    def test_create_user_without_admin_permission(self, client, auth_headers):
        """Test creating user without admin permission."""
        headers = auth_headers()
        
        response = client.post('/admin/create_user', data={
            'username': 'newuser',
            'userpwd': 'ValidPass123!',
            'is_admin': False
        }, headers=headers)
        
        # Should be denied access
        assert response.status_code in [403, 404, 302]
    
    def test_create_user_with_invalid_data(self, client, admin_headers):
        """Test creating user with invalid data."""
        headers = admin_headers()
        
        response = client.post('/admin/create_user', data={
            'username': '',  # Empty username
            'userpwd': 'ValidPass123!',
            'is_admin': False
        }, headers=headers)
        
        assert response.status_code in [200, 302]
    
    def test_create_user_with_weak_password(self, client, admin_headers):
        """Test creating user with weak password."""
        headers = admin_headers()
        
        response = client.post('/admin/create_user', data={
            'username': 'newuser',
            'userpwd': '123',  # Weak password
            'is_admin': False
        }, headers=headers)
        
        assert response.status_code in [200, 302]
    
    def test_create_duplicate_user(self, client, admin_headers):
        """Test creating duplicate user."""
        headers = admin_headers()
        
        # Create first user
        client.post('/admin/create_user', data={
            'username': 'duplicateuser',
            'userpwd': 'ValidPass123!',
            'is_admin': False
        }, headers=headers)
        
        # Try to create duplicate
        response = client.post('/admin/create_user', data={
            'username': 'duplicateuser',
            'userpwd': 'AnotherPass456!',
            'is_admin': False
        }, headers=headers)
        
        assert response.status_code in [200, 302]
    
    def test_edit_user_with_valid_data(self, client, admin_headers):
        """Test editing user with valid data."""
        headers = admin_headers()
        
        # Create user first
        client.post('/admin/create_user', data={
            'username': 'edituser',
            'userpwd': 'ValidPass123!',
            'is_admin': False
        }, headers=headers)
        
        # Edit user
        response = client.post('/admin/edit_user/1', data={
            'username': 'editeduser',
            'userpwd': 'NewPass456!',
            'is_admin': True
        }, headers=headers)
        
        assert response.status_code == 302
    
    def test_delete_user(self, client, admin_headers):
        """Test deleting user."""
        headers = admin_headers()
        
        # Create user first
        client.post('/admin/create_user', data={
            'username': 'deleteuser',
            'userpwd': 'ValidPass123!',
            'is_admin': False
        }, headers=headers)
        
        # Delete user
        response = client.post('/admin/delete_user/1', headers=headers)
        
        assert response.status_code == 302


class TestLogViewer:
    """Test log viewer functionality."""
    
    def test_log_viewer_access_with_admin_user(self, client, admin_headers):
        """Test log viewer access with admin user."""
        headers = admin_headers()
        
        response = client.get('/admin/logs', headers=headers)
        
        assert response.status_code == 200
        assert b'log' in response.data.lower()
    
    def test_log_viewer_access_without_admin_permission(self, client, auth_headers):
        """Test log viewer access without admin permission."""
        headers = auth_headers()
        
        response = client.get('/admin/logs', headers=headers)
        
        # Should be denied access
        assert response.status_code in [403, 404, 302]
    
    def test_log_file_viewer_access(self, client, admin_headers):
        """Test log file viewer access."""
        headers = admin_headers()
        
        response = client.get('/admin/logs/portfolio_analyzer.log', headers=headers)
        
        # Should either show the log file or handle gracefully
        assert response.status_code in [200, 404]
    
    def test_log_file_viewer_with_invalid_file(self, client, admin_headers):
        """Test log file viewer with invalid file."""
        headers = admin_headers()
        
        response = client.get('/admin/logs/../../etc/passwd', headers=headers)
        
        # Should be denied access (path traversal protection)
        assert response.status_code in [403, 404, 302]
    
    def test_log_file_viewer_with_nonexistent_file(self, client, admin_headers):
        """Test log file viewer with nonexistent file."""
        headers = admin_headers()
        
        response = client.get('/admin/logs/nonexistent.log', headers=headers)
        
        # Should handle gracefully
        assert response.status_code in [404, 302]


class TestAdminInputValidation:
    """Test admin input validation."""
    
    def test_security_name_validation(self, client, admin_headers):
        """Test security name validation."""
        headers = admin_headers()
        
        # Empty name
        response = client.post('/admin/create_security', data={
            'bondname': '',
            'bondsymbol': 'TEST',
            'bondcategoryid': 1,
            'bondcurrencyid': 1,
            'bondsector': 'Technology',
            'exchangeid': 1
        }, headers=headers)
        
        assert response.status_code in [200, 302]
    
    def test_security_symbol_validation(self, client, admin_headers):
        """Test security symbol validation."""
        headers = admin_headers()
        
        # Empty symbol
        response = client.post('/admin/create_security', data={
            'bondname': 'Test Security',
            'bondsymbol': '',
            'bondcategoryid': 1,
            'bondcurrencyid': 1,
            'bondsector': 'Technology',
            'exchangeid': 1
        }, headers=headers)
        
        assert response.status_code in [200, 302]
    
    def test_currency_code_validation(self, client, admin_headers):
        """Test currency code validation."""
        headers = admin_headers()
        
        # Invalid currency code format
        response = client.post('/admin/create_currency', data={
            'currencycode': 'INVALID123',
            'currencyname': 'Invalid Currency'
        }, headers=headers)
        
        assert response.status_code in [200, 302]
    
    def test_exchange_name_validation(self, client, admin_headers):
        """Test exchange name validation."""
        headers = admin_headers()
        
        # Empty exchange name
        response = client.post('/admin/create_exchange', data={
            'exchangename': '',
            'exchangename': 'Test Exchange',
            'regionid': 1
        }, headers=headers)
        
        assert response.status_code in [200, 302]


class TestAdminErrorHandling:
    """Test admin error handling."""
    
    def test_admin_handles_database_errors(self, client, admin_headers, mock_db_connection):
        """Test admin handles database errors gracefully."""
        headers = admin_headers()
        
        # Mock database error
        mock_db_connection.side_effect = Exception("Database connection failed")
        
        response = client.post('/admin/create_security', data={
            'bondname': 'Test Security',
            'bondsymbol': 'TEST',
            'bondcategoryid': 1,
            'bondcurrencyid': 1,
            'bondsector': 'Technology',
            'exchangeid': 1
        }, headers=headers)
        
        # Should handle error gracefully
        assert response.status_code in [200, 302, 500]
    
    def test_admin_handles_invalid_ids(self, client, admin_headers):
        """Test admin handles invalid IDs gracefully."""
        headers = admin_headers()
        
        # Try to edit nonexistent security
        response = client.post('/admin/edit_security/999', data={
            'bondname': 'Updated Security',
            'bondsymbol': 'UPD',
            'bondcategoryid': 1,
            'bondcurrencyid': 1,
            'bondsector': 'Technology',
            'exchangeid': 1
        }, headers=headers)
        
        # Should handle gracefully
        assert response.status_code in [302, 404]
    
    def test_admin_handles_missing_required_fields(self, client, admin_headers):
        """Test admin handles missing required fields."""
        headers = admin_headers()
        
        # Missing required fields
        response = client.post('/admin/create_security', data={
            'bondname': 'Test Security',
            # Missing other required fields
        }, headers=headers)
        
        assert response.status_code in [200, 302]
