-- MySQL initialization script for Portfolio Analyzer
-- This script ensures proper user setup and authentication

-- Create the application user if it doesn't exist
CREATE USER IF NOT EXISTS 'portfolio_app'@'%' IDENTIFIED BY '${DB_PASSWORD}';

-- Grant necessary privileges
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER, REFERENCES, TRIGGER ON portfolioanalyzer.* TO 'portfolio_app'@'%';
GRANT CREATE ON *.* TO 'portfolio_app'@'%';
GRANT SUPER, PROCESS ON *.* TO 'portfolio_app'@'%';
GRANT EXECUTE ON portfolioanalyzer.* TO 'portfolio_app'@'%';
GRANT CREATE ROUTINE, ALTER ROUTINE ON portfolioanalyzer.* TO 'portfolio_app'@'%';

-- Flush privileges to ensure they take effect
FLUSH PRIVILEGES;
