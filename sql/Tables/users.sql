USE portfolioanalyzer;

CREATE TABLE users (
    userid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    userpwd VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);