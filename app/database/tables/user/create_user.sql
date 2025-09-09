USE portfolioanalyzer;

CREATE TABLE user (
    userid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    userpwd VARCHAR(255) NOT NULL,
    email VARCHAR(255) DEFAULT 'N/A',
    default_base_currency INT DEFAULT 1,
    is_admin BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (default_base_currency) REFERENCES currency(currencyid)
);