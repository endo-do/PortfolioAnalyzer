# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [2025-09-10]

### Added
- Resolution based content scaling
- API Management dashboard with comprehensive fetch monitoring and manual controls
- Bulk API fetch logging system for exchange rates and security rates
- Individual API fetch retry functionality with loading modals
- Failed fetch tracking and retry mechanism with attempt limits
- API statistics dashboard showing total, successful, and failed fetches
- Manual fetch controls for both individual and bulk operations
- Recent API fetches table with filtering and status indicators

### Improved
- Console output cleanliness by suppressing yfinance HTTP 404 errors and warnings
- Error handling in API fetch operations with proper logging
- Daily exchange- and securityrate updates at 0.00h
- UI tweaks for faster performance


## [2025-09-09]

### Added
- Account creation date tracking with `created_at` timestamp display in settings
- Consistent filter layouts across all pages (Sort By → Category → Region → Sector)
- Complete UI redesign with modern card-based layouts and Font Awesome icons
- Comprehensive breadcrumb navigation system across all pages
- Modern notification system with animated slide-in notifications
- New settings page with account management and user preferences
- Advanced filtering and sorting options for securities, currencies, and exchanges
- User-friendly database setup script for new installations

### Fixed
- Portfolio view currency conversion to show portfolio native currency instead of user base currency
- Home page pie chart colors to match table colors for consistent visual hierarchy
- Empty state handling with proper "100%" display for empty portfolios and disabled legends
- Database setup process to work for new users without existing database
- Currency conversion issues across all portfolio and security views

### Reworked
- Admin dashboard, security overview, user management, and exchange management pages
- Home page with statistics cards and portfolio management section
- Portfolio view page with professional header and 3-column breakdown layout
- Modal designs with modern styling and improved user interaction
- Currency conversion system with proper base currency handling

## [2025-09-08]

### Fixed
- Fixed all 228 test cases - comprehensive test suite now fully passing
- Fixed inconsistent API test failures and endpoint routing issues
- Fixed login/logout workflows and session management
- Fixed input validation test cases that were getting stuck
- Fixed logging test failures and permission errors

### Added
- Enhanced security with CSRF protection and input validation
- Comprehensive error handling throughout the application

### Improved
- Reduced test execution time from 60+ seconds to under 1 second
- Enhanced data validation and transaction handling
- Removed debug code and improved error messages for better UX

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
