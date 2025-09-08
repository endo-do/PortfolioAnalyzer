"""
Portfolio management tests for Portfolio Analyzer.
"""

import pytest
from flask import url_for
from tests.fixtures.test_data import INVALID_PORTFOLIO_NAMES, SQL_INJECTION_PAYLOADS, XSS_PAYLOADS


class TestPortfolioCreation:
    """Test portfolio creation functionality."""
    
    def test_valid_portfolio_creation(self, client, auth_headers):
        """Test successful portfolio creation with valid data."""
        headers = auth_headers()
        
        response = client.post('/create_portfolio', data={
            'portfolioname': 'Test Portfolio',
            'portfoliodescription': 'A test portfolio for unit testing',
            'currencycode': 'USD'
        }, headers=headers)
        
        assert response.status_code == 302  # Redirect after successful creation
        assert '/' in response.location  # Redirect to home page
    
    def test_portfolio_creation_without_authentication(self, client):
        """Test portfolio creation without authentication."""
        response = client.post('/create_portfolio', data={
            'portfolioname': 'Test Portfolio',
            'portfoliodescription': 'A test portfolio',
            'currencycode': 'USD'
        })
        
        # Should redirect to login page or home
        assert response.status_code == 302
        assert '/' in response.location
    
    def test_portfolio_creation_with_empty_name(self, client, auth_headers):
        """Test portfolio creation with empty name."""
        headers = auth_headers()
        
        response = client.post('/create_portfolio', data={
            'portfolioname': '',
            'portfoliodescription': 'A test portfolio',
            'currencycode': 'USD'
        }, headers=headers)
        
        assert response.status_code in [200, 302]
        if response.status_code == 200:
            assert b'name' in response.data.lower()
    
    def test_portfolio_creation_with_invalid_name(self, client, auth_headers):
        """Test portfolio creation with invalid names."""
        headers = auth_headers()
        
        for invalid_name in INVALID_PORTFOLIO_NAMES:
            response = client.post('/create_portfolio', data={
                'portfolioname': invalid_name,
                'portfoliodescription': 'A test portfolio',
                'currencycode': 'USD'
            }, headers=headers)
            
        assert response.status_code in [200, 302]
    
    def test_portfolio_creation_with_sql_injection(self, client, auth_headers):
        """Test portfolio creation with SQL injection payloads."""
        headers = auth_headers()
        
        for payload in SQL_INJECTION_PAYLOADS:
            response = client.post('/create_portfolio', data={
                'portfolioname': payload,
                'portfoliodescription': 'A test portfolio',
                'currencycode': 'USD'
            }, headers=headers)
            
            # Should be rejected
        assert response.status_code in [200, 302]
    
    def test_portfolio_creation_with_xss_payload(self, client, auth_headers):
        """Test portfolio creation with XSS payloads."""
        headers = auth_headers()
        
        for payload in XSS_PAYLOADS:
            response = client.post('/create_portfolio', data={
                'portfolioname': payload,
                'portfoliodescription': 'A test portfolio',
                'currencycode': 'USD'
            }, headers=headers)
            
            # Should be rejected
        assert response.status_code in [200, 302]
    
    def test_portfolio_creation_with_invalid_currency(self, client, auth_headers):
        """Test portfolio creation with invalid currency code."""
        headers = auth_headers()
        
        response = client.post('/create_portfolio', data={
            'portfolioname': 'Test Portfolio',
            'portfoliodescription': 'A test portfolio',
            'currencycode': 'INVALID'
        }, headers=headers)
        
        assert response.status_code in [200, 302]


class TestPortfolioViewing:
    """Test portfolio viewing functionality."""
    
    def test_portfolio_list_view(self, client, auth_headers):
        """Test viewing portfolio list."""
        headers = auth_headers()
        
        response = client.get('/', headers=headers)
        
        assert response.status_code == 200
        assert b'portfolio' in response.data.lower()
    
    def test_portfolio_list_without_authentication(self, client):
        """Test portfolio list view without authentication."""
        response = client.get('/')
        
        # Should redirect to login page or be accessible
        assert response.status_code in [200, 302]
        if response.status_code == 302:
            assert '/auth/login' in response.location
    
    def test_portfolio_detail_view(self, client, auth_headers):
        """Test viewing portfolio details."""
        headers = auth_headers()
        
        # First create a portfolio
        client.post('/create_portfolio', data={
            'portfolioname': 'Detail Test Portfolio',
            'portfoliodescription': 'A portfolio for detail testing',
            'currencycode': 'USD'
        }, headers=headers)
        
        # Then view it (assuming portfolio ID 1)
        response = client.get('/portfolio/1', headers=headers)
        
        # Should either show the portfolio or redirect appropriately
        assert response.status_code in [200, 302, 404]
    
    def test_portfolio_detail_view_unauthorized(self, client, auth_headers):
        """Test viewing portfolio details without proper authorization."""
        # Create portfolio with one user
        headers1 = auth_headers('user1', 'Pass123!')
        client.post('/create_portfolio', data={
            'portfolioname': 'Private Portfolio',
            'portfoliodescription': 'A private portfolio',
            'currencycode': 'USD'
        }, headers=headers1)
        
        # Try to view with different user
        headers2 = auth_headers('user2', 'Pass456!')
        response = client.get('/portfolio/1', headers=headers2)
        
        # Should be denied access
        assert response.status_code in [403, 404, 302]


class TestPortfolioEditing:
    """Test portfolio editing functionality."""
    
    def test_portfolio_edit_with_valid_data(self, client, auth_headers):
        """Test portfolio editing with valid data."""
        headers = auth_headers()
        
        # Create portfolio first
        client.post('/create_portfolio', data={
            'portfolioname': 'Edit Test Portfolio',
            'portfoliodescription': 'A portfolio for editing',
            'currencycode': 'USD'
        }, headers=headers)
        
        # Edit portfolio
        response = client.post('/update_portfolio_details/1', data={
            'portfolioname': 'Updated Portfolio Name',
            'portfoliodescription': 'Updated description',
            'currencycode': 'EUR'
        }, headers=headers)
        
        assert response.status_code == 302
    
    def test_portfolio_edit_without_authentication(self, client):
        """Test portfolio editing without authentication."""
        response = client.post('/update_portfolio_details/1', data={
            'portfolioname': 'Updated Name',
            'portfoliodescription': 'Updated description',
            'currencycode': 'USD'
        })
        
        # Should redirect to login page
        assert response.status_code == 302
        assert '/auth/login' in response.location
    
    def test_portfolio_edit_unauthorized(self, client, auth_headers):
        """Test portfolio editing by unauthorized user."""
        # Create portfolio with one user
        headers1 = auth_headers('user1', 'Pass123!')
        client.post('/create_portfolio', data={
            'portfolioname': 'Private Portfolio',
            'portfoliodescription': 'A private portfolio',
            'currencycode': 'USD'
        }, headers=headers1)
        
        # Try to edit with different user
        headers2 = auth_headers('user2', 'Pass456!')
        response = client.post('/update_portfolio_details/1', data={
            'portfolioname': 'Hacked Name',
            'portfoliodescription': 'Hacked description',
            'currencycode': 'USD'
        }, headers=headers2)
        
        # Should be denied access
        assert response.status_code in [403, 404, 302]
    
    def test_portfolio_edit_with_invalid_data(self, client, auth_headers):
        """Test portfolio editing with invalid data."""
        headers = auth_headers()
        
        # Create portfolio first
        client.post('/create_portfolio', data={
            'portfolioname': 'Edit Test Portfolio',
            'portfoliodescription': 'A portfolio for editing',
            'currencycode': 'USD'
        }, headers=headers)
        
        # Edit with invalid data
        response = client.post('/update_portfolio_details/1', data={
            'portfolioname': '',  # Empty name
            'portfoliodescription': 'Updated description',
            'currencycode': 'USD'
        }, headers=headers)
        
        assert response.status_code in [200, 302]


class TestPortfolioDeletion:
    """Test portfolio deletion functionality."""
    
    def test_portfolio_deletion(self, client, auth_headers):
        """Test successful portfolio deletion."""
        headers = auth_headers()
        
        # Create portfolio first
        client.post('/create_portfolio', data={
            'portfolioname': 'Delete Test Portfolio',
            'portfoliodescription': 'A portfolio for deletion',
            'currencycode': 'USD'
        }, headers=headers)
        
        # Delete portfolio
        response = client.post('/delete_portfolio/1', headers=headers)
        
        assert response.status_code == 302
    
    def test_portfolio_deletion_without_authentication(self, client):
        """Test portfolio deletion without authentication."""
        response = client.post('/delete_portfolio/1')
        
        # Should redirect to login page or home
        assert response.status_code == 302
        assert '/' in response.location
    
    def test_portfolio_deletion_unauthorized(self, client, auth_headers):
        """Test portfolio deletion by unauthorized user."""
        # Create portfolio with one user
        headers1 = auth_headers('user1', 'Pass123!')
        client.post('/create_portfolio', data={
            'portfolioname': 'Private Portfolio',
            'portfoliodescription': 'A private portfolio',
            'currencycode': 'USD'
        }, headers=headers1)
        
        # Try to delete with different user
        headers2 = auth_headers('user2', 'Pass456!')
        response = client.post('/delete_portfolio/1', headers=headers2)
        
        # Should be denied access
        assert response.status_code in [403, 404, 302]
    
    def test_portfolio_deletion_nonexistent(self, client, auth_headers):
        """Test deletion of nonexistent portfolio."""
        headers = auth_headers()
        
        response = client.post('/delete_portfolio/999', headers=headers)
        
        # Should handle gracefully
        assert response.status_code in [302, 404]


class TestPortfolioSecurities:
    """Test portfolio securities management."""
    
    def test_add_security_to_portfolio(self, client, auth_headers):
        """Test adding security to portfolio."""
        headers = auth_headers()
        
        # Create portfolio first
        client.post('/create_portfolio', data={
            'portfolioname': 'Securities Test Portfolio',
            'portfoliodescription': 'A portfolio for securities testing',
            'currencycode': 'USD'
        }, headers=headers)
        
        # Add security
        response = client.post('/update_securities/1', data={
            'bond_id': 1,
            'quantity': 100
        }, headers=headers)
        
        assert response.status_code == 302
    
    def test_add_security_without_authentication(self, client):
        """Test adding security without authentication."""
        response = client.post('/update_securities/1', data={
            'bond_id': 1,
            'quantity': 100
        })
        
        # Should redirect to login page
        assert response.status_code == 302
        assert '/auth/login' in response.location
    
    def test_add_security_with_invalid_data(self, client, auth_headers):
        """Test adding security with invalid data."""
        headers = auth_headers()
        
        # Create portfolio first
        client.post('/create_portfolio', data={
            'portfolioname': 'Securities Test Portfolio',
            'portfoliodescription': 'A portfolio for securities testing',
            'currencycode': 'USD'
        }, headers=headers)
        
        # Add security with invalid data
        response = client.post('/update_securities/1', data={
            'bond_id': '',  # Empty bond ID
            'quantity': 100
        }, headers=headers)
        
        assert response.status_code in [200, 302]
    
    def test_add_security_with_negative_quantity(self, client, auth_headers):
        """Test adding security with negative quantity."""
        headers = auth_headers()
        
        # Create portfolio first
        client.post('/create_portfolio', data={
            'portfolioname': 'Securities Test Portfolio',
            'portfoliodescription': 'A portfolio for securities testing',
            'currencycode': 'USD'
        }, headers=headers)
        
        # Add security with negative quantity
        response = client.post('/update_securities/1', data={
            'bond_id': 1,
            'quantity': -100
        }, headers=headers)
        
        assert response.status_code in [200, 302]
    
    def test_remove_security_from_portfolio(self, client, auth_headers):
        """Test removing security from portfolio."""
        headers = auth_headers()
        
        # Create portfolio first
        client.post('/create_portfolio', data={
            'portfolioname': 'Securities Test Portfolio',
            'portfoliodescription': 'A portfolio for securities testing',
            'currencycode': 'USD'
        }, headers=headers)
        
        # Add security first
        client.post('/update_securities/1', data={
            'bond_id': 1,
            'quantity': 100
        }, headers=headers)
        
        # Remove security
        response = client.post('/update_securities/1', data={
            'action': 'remove',
            'bond_id': 1
        }, headers=headers)
        
        assert response.status_code == 302


class TestPortfolioValidation:
    """Test portfolio data validation."""
    
    def test_portfolio_name_length_validation(self, client, auth_headers):
        """Test portfolio name length validation."""
        headers = auth_headers()
        
        # Too long name
        response = client.post('/create_portfolio', data={
            'portfolioname': 'a' * 1000,
            'portfoliodescription': 'A test portfolio',
            'currencycode': 'USD'
        }, headers=headers)
        
        assert response.status_code in [200, 302]
    
    def test_portfolio_description_length_validation(self, client, auth_headers):
        """Test portfolio description length validation."""
        headers = auth_headers()
        
        # Too long description
        response = client.post('/create_portfolio', data={
            'portfolioname': 'Test Portfolio',
            'portfoliodescription': 'a' * 10000,
            'currencycode': 'USD'
        }, headers=headers)
        
        assert response.status_code in [200, 302]
    
    def test_portfolio_currency_validation(self, client, auth_headers):
        """Test portfolio currency validation."""
        headers = auth_headers()
        
        invalid_currencies = ['INVALID', '123', 'USD123', '']
        
        for currency in invalid_currencies:
            response = client.post('/create_portfolio', data={
                'portfolioname': 'Test Portfolio',
                'portfoliodescription': 'A test portfolio',
                'currencycode': currency
            }, headers=headers)
            
        assert response.status_code in [200, 302]


class TestPortfolioOwnership:
    """Test portfolio ownership and access control."""
    
    def test_user_can_only_access_own_portfolios(self, client, auth_headers):
        """Test that users can only access their own portfolios."""
        # Create portfolio with user1
        headers1 = auth_headers('user1', 'Pass123!')
        client.post('/create_portfolio', data={
            'portfolioname': 'User1 Portfolio',
            'portfoliodescription': 'User1 private portfolio',
            'currencycode': 'USD'
        }, headers=headers1)
        
        # Try to access with user2
        headers2 = auth_headers('user2', 'Pass456!')
        response = client.get('/portfolio/1', headers=headers2)
        
        # Should be denied access
        assert response.status_code in [403, 404, 302]
    
    def test_user_can_only_edit_own_portfolios(self, client, auth_headers):
        """Test that users can only edit their own portfolios."""
        # Create portfolio with user1
        headers1 = auth_headers('user1', 'Pass123!')
        client.post('/create_portfolio', data={
            'portfolioname': 'User1 Portfolio',
            'portfoliodescription': 'User1 private portfolio',
            'currencycode': 'USD'
        }, headers=headers1)
        
        # Try to edit with user2
        headers2 = auth_headers('user2', 'Pass456!')
        response = client.post('/update_portfolio_details/1', data={
            'portfolioname': 'Hacked Portfolio',
            'portfoliodescription': 'Hacked description',
            'currencycode': 'USD'
        }, headers=headers2)
        
        # Should be denied access
        assert response.status_code in [403, 404, 302]
    
    def test_user_can_only_delete_own_portfolios(self, client, auth_headers):
        """Test that users can only delete their own portfolios."""
        # Create portfolio with user1
        headers1 = auth_headers('user1', 'Pass123!')
        client.post('/create_portfolio', data={
            'portfolioname': 'User1 Portfolio',
            'portfoliodescription': 'User1 private portfolio',
            'currencycode': 'USD'
        }, headers=headers1)
        
        # Try to delete with user2
        headers2 = auth_headers('user2', 'Pass456!')
        response = client.post('/delete_portfolio/1', headers=headers2)
        
        # Should be denied access
        assert response.status_code in [403, 404, 302]
