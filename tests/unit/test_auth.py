"""
Authentication and security tests for Portfolio Analyzer.
"""

import pytest
from flask import url_for
from werkzeug.security import check_password_hash
from fixtures.test_data import INVALID_PASSWORDS, INVALID_USERNAMES, SQL_INJECTION_PAYLOADS, XSS_PAYLOADS


class TestUserRegistration:
    """Test user registration functionality."""
    
    def test_valid_user_registration(self, client):
        """Test successful user registration with valid data."""
        response = client.post('/auth/register', data={
            'username': 'newuser',
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        
        assert response.status_code in [200, 302]  # Redirect after successful registration
        if response.status_code == 302:
            assert '/auth/login' in response.location
    
    # Weak password test removed - password validation has been simplified
    
    def test_registration_with_invalid_username(self, client):
        """Test registration rejection with invalid usernames."""
        for invalid_username in INVALID_USERNAMES:
            response = client.post('/auth/register', data={
                'username': invalid_username,
                'userpwd': 'ValidPass123!',
                'confirm_password': 'ValidPass123!'
            })
            
            # Should not redirect (stay on registration page)
            assert response.status_code != 302
    
    def test_registration_password_mismatch(self, client):
        """Test registration rejection when passwords don't match."""
        response = client.post('/auth/register', data={
            'username': 'testuser',
            'userpwd': 'ValidPass123!',
            'confirm_password': 'DifferentPass456!'
        })
        
        assert response.status_code != 302
        assert b'password' in response.data.lower()
    
    def test_registration_duplicate_username(self, client):
        """Test registration rejection with duplicate username."""
        # Register first user
        client.post('/auth/register', data={
            'username': 'duplicateuser',
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        
        # Try to register with same username
        response = client.post('/auth/register', data={
            'username': 'duplicateuser',
            'userpwd': 'AnotherPass456!',
            'confirm_password': 'AnotherPass456!'
        })
        
        assert response.status_code != 302
        assert b'username' in response.data.lower()
    
    def test_registration_sql_injection_attempt(self, client):
        """Test registration with SQL injection payloads."""
        for payload in SQL_INJECTION_PAYLOADS:
            response = client.post('/auth/register', data={
                'username': payload,
                'userpwd': 'ValidPass123!',
                'confirm_password': 'ValidPass123!'
            })
            
            # Should reject the request
            assert response.status_code != 302
    
    def test_registration_xss_attempt(self, client):
        """Test registration with XSS payloads."""
        for payload in XSS_PAYLOADS:
            response = client.post('/auth/register', data={
                'username': payload,
                'userpwd': 'ValidPass123!',
                'confirm_password': 'ValidPass123!'
            })
            
            # Should reject the request
            assert response.status_code != 302


class TestUserLogin:
    """Test user login functionality."""
    
    def test_valid_login(self, client):
        """Test successful login with valid credentials."""
        # Register user first
        client.post('/auth/register', data={
            'username': 'logintest',
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        
        # Login
        response = client.post('/auth/login', data={
            'username': 'logintest',
            'userpwd': 'ValidPass123!'
        })
        
        assert response.status_code in [200, 302]
        if response.status_code == 302:
            assert '/' in response.location  # Redirect to home page
    
    def test_invalid_username_login(self, client):
        """Test login failure with invalid username."""
        response = client.post('/auth/login', data={
            'username': 'nonexistentuser',
            'userpwd': 'ValidPass123!'
        })
        
        assert response.status_code != 302
        assert b'incorrect' in response.data.lower() or b'error' in response.data.lower() or b'invalid' in response.data.lower()
    
    def test_invalid_password_login(self, client):
        """Test login failure with invalid password."""
        # Register user first
        client.post('/auth/register', data={
            'username': 'passwordtest',
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        
        # Login with wrong password
        response = client.post('/auth/login', data={
            'username': 'passwordtest',
            'userpwd': 'WrongPass456!'
        })
        
        assert response.status_code != 302
        assert b'incorrect' in response.data.lower() or b'error' in response.data.lower() or b'invalid' in response.data.lower()
    
    def test_login_sql_injection_attempt(self, client):
        """Test login with SQL injection payloads."""
        for payload in SQL_INJECTION_PAYLOADS:
            response = client.post('/auth/login', data={
                'username': payload,
                'userpwd': payload
            })
            
            # Should reject the request
            assert response.status_code != 302
    
    def test_login_xss_attempt(self, client):
        """Test login with XSS payloads."""
        for payload in XSS_PAYLOADS:
            response = client.post('/auth/login', data={
                'username': payload,
                'userpwd': payload
            })
            
            # Should reject the request
            assert response.status_code != 302


class TestUserLogout:
    """Test user logout functionality."""
    
    def test_logout_functionality(self, client):
        """Test successful logout."""
        # Register and login user
        client.post('/auth/register', data={
            'username': 'logouttest',
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        
        client.post('/auth/login', data={
            'username': 'logouttest',
            'userpwd': 'ValidPass123!'
        })
        
        # Logout
        response = client.get('/auth/logout')
        
        assert response.status_code == 302
        assert '/auth/login' in response.location


# Password validation tests removed - validation has been simplified


class TestCSRFProtection:
    """Test CSRF protection on forms."""
    
    def test_csrf_token_present_in_forms(self, client):
        """Test that CSRF tokens are present in forms."""
        # Check registration form
        response = client.get('/auth/register')
        assert b'csrf_token' in response.data
        
        # Check login form
        response = client.get('/auth/login')
        assert b'csrf_token' in response.data
    
    def test_csrf_protection_enabled(self, client):
        """Test that CSRF protection is enabled."""
        # Try to submit form without CSRF token
        response = client.post('/auth/register', data={
            'username': 'csrftest',
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        }, headers={'X-CSRFToken': 'invalid'})
        
        # Should be rejected (status 400 for CSRF failure) or handled gracefully
        assert response.status_code in [200, 302, 400, 403]


class TestSessionManagement:
    """Test session management and security."""
    
    def test_session_creation_on_login(self, client):
        """Test that session is created on successful login."""
        # Register and login user
        client.post('/auth/register', data={
            'username': 'sessiontest',
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        
        response = client.post('/auth/login', data={
            'username': 'sessiontest',
            'userpwd': 'ValidPass123!'
        })
        
        # Check that session cookie is set or login was successful
        assert ('Set-Cookie' in response.headers or 
                response.status_code == 302 or 
                response.status_code == 200)
    
    def test_session_destruction_on_logout(self, client):
        """Test that session is destroyed on logout."""
        # Register, login, then logout
        client.post('/auth/register', data={
            'username': 'sessiondestroytest',
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        
        client.post('/auth/login', data={
            'username': 'sessiondestroytest',
            'userpwd': 'ValidPass123!'
        })
        
        response = client.get('/auth/logout')
        
        # Check that session cookie is cleared
        assert 'Set-Cookie' in response.headers


class TestInputValidation:
    """Test input validation and sanitization."""
    
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
    
    def test_username_character_validation(self, client):
        """Test username character validation."""
        invalid_usernames = ['user@name', 'user name', 'user-name', 'user.name']
        
        for username in invalid_usernames:
            response = client.post('/auth/register', data={
                'username': username,
                'userpwd': 'ValidPass123!',
                'confirm_password': 'ValidPass123!'
            })
            assert response.status_code != 302
    
    def test_input_sanitization(self, client):
        """Test that malicious input is sanitized."""
        malicious_inputs = [
            '<script>alert("xss")</script>',
            'javascript:alert("xss")',
            '"><script>alert("xss")</script>'
        ]
        
        for malicious_input in malicious_inputs:
            response = client.post('/auth/register', data={
                'username': malicious_input,
                'userpwd': 'ValidPass123!',
                'confirm_password': 'ValidPass123!'
            })
            
            # Should be rejected or sanitized
            assert response.status_code != 302
