-- Create application user for Portfolio Analyzer
-- This script should be run as MySQL root user

-- Create the application user
CREATE USER IF NOT EXISTS 'portfolio_app'@'%' IDENTIFIED BY '${DB_PASSWORD}';

-- Grant necessary privileges to the application user
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER, REFERENCES, TRIGGER ON ${DB_NAME}.* TO 'portfolio_app'@'%';

-- Grant privileges for creating databases (needed for initial setup)
GRANT CREATE ON *.* TO 'portfolio_app'@'%';

-- Grant additional privileges needed for triggers and procedures
GRANT SUPER, PROCESS ON *.* TO 'portfolio_app'@'%';

-- Grant privileges for stored procedures and functions
GRANT EXECUTE ON ${DB_NAME}.* TO 'portfolio_app'@'%';
GRANT CREATE ROUTINE, ALTER ROUTINE ON ${DB_NAME}.* TO 'portfolio_app'@'%';

-- Apply the changes
FLUSH PRIVILEGES;

-- Show the created user
SELECT User, Host FROM mysql.user WHERE User = 'portfolio_app';
