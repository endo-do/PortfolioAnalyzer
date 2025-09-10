CREATE TABLE currency (
    currencyid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    currencyname VARCHAR(50) NOT NULL,
    currencycode VARCHAR(50) NOT NULL UNIQUE
);