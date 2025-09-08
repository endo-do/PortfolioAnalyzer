# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [2025-01-27]

### Added
- Comprehensive error handling throughout the application
- Input validation and sanitization for all forms
- CSRF protection with Flask-WTF
- User permission checks for portfolio operations
- Form data validation with length limits and format checks
- Database error handling with proper rollback mechanisms

### Fixed
- Removed all debug code (input() statements) from production code
- Fixed potential security vulnerabilities in form handling
- Fixed CSRF token display issue on login/registration forms
- Fixed Jinja2 datetime filter error in admin log viewer template
- Fixed current_user import issue in global exception handler
- Fixed datetime formatting in log viewer (float timestamp conversion)
- Fixed current_user import in admin routes for proper error logging
- Improved error messages for better user experience
- Enhanced data integrity with proper validation

### Security
- Implemented CSRF tokens for all forms
- Added input sanitization to prevent malicious data
- Enhanced user permission verification
- Improved error handling to prevent information leakage

### Dependencies
- Added Flask-WTF==1.2.1 for CSRF protection
- Added WTForms==3.1.1 for form validation

### Logging & Monitoring
- Implemented comprehensive logging system with file rotation
- Added structured logging for user actions, security events, and errors
- Created admin log viewer with web interface
- Added password strength validation and requirements
- Implemented security event tracking and monitoring

## [2025-08-17]

### Added
- Region and sector allocation in portfolioview
- Exchange management including creation, editing and deletion
- Exchange assignment at security creation
- Region, sector and exchange tables
- Back button / 404 Handeling
- Pie Chart legend outside the canvas

### Reworked
- Pie chart size consistency
- Pie chart coloring
- Pie chart labels
- Table coloring

## [2025-07-18]

### Added
- Added advanced error handling
- Added flash feedback messages on e.g. portfolio creation

### Reworked
- Minor UI changes

## [2025-07-17]

### Added
- Added Security-Management in adminview
- Added Currency-Management in adminview
- Added User-Management in adminview
- Added pie charts for portfolioview and home

### Reworked
- Reworked testdata insertion simplified with api routes

## [2025-07-16]

### Added
- Daily scheduled exchangerate and securityrate updates
- Delete portfolio option in portfolioview
- Create portfolio option in home
- Securityview route

### Reworked
- switches from twelvedata API to yfinance

## [2025-07-12]
### Added
- edit_portfolio endpoint to add, delete and manage quantity of securities in a portfolio
  
### Reworked
- Some small UI tweaks

### Restructured
- Moved the JS code from the html into sperate files

## [2025-07-10]
### Added
- Added the portfolioview endpoint for more detailed info on a portfolio
- Added the admin endpoint which will later be used to add, edit or delete bonds
- Added a admin user that has acces to the admin endpoint

### Reworked
- Reworked the entire UI using bootstrap
- Reworked the database connection handling

## [2025-06-02]
### Resctructered
- Split up database creation into seprate files

### Added
- Easier database setup with run_setup.batch
- Real testdata in sql/Data
- Usage section in README

### Moved
- Moved the bondcategory creation into sql/data

## [2025-05-30]
### Resctructered
- Split up SQL files into more organized sub dirs

## [2025-05-26]
### Added
- Bond data fetching

### Optimized
- Improved exchange rate API usage and refactored internal structure.

## [2025-05-25]
### Added
- API request queue system.
- Basic CSS styling for UI.

### Fixed
- Exchange rate logic now correctly handles all cases.

### Enhanced
- Portfolio display now includes value by bond category.

## [2025-05-22]
### Added
- Connection pooling for more efficient database access.
- Began implementation of detailed portfolio view.

## [2025-05-21]
### Added
- Integrated Exchange Rates API.

## [2025-05-19]
### Added
- Total portfolio value calculation using up-to-date bond and exchange rates.
- Basic login and registration functionality with hashed passwords.
- User's portfolio overview on the homepage.

## [2025-05-18]
### Added
- Initial project structure and MySQL database layout.
- Started on portfolio value calculation logic.
