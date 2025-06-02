# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

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
