DROP DATABASE IF EXISTS bondanalyser;
CREATE DATABASE bondanalyser;
USE bondanalyser;
CREATE TABLE users (
    userid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    userpwd VARCHAR(300) NOT NULL
);
CREATE TABLE currencies (
    currencyid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    currencyname VARCHAR(50) NOT NULL
);
CREATE TABLE portfolios (
    portfolioid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    userid INT NOT NULL,
    portfoliodescription VARCHAR(50),
    portfoliocurrencyid INT NOT NULL,
    FOREIGN KEY (userid) REFERENCES users (userid),
    FOREIGN KEY (portfoliocurrencyid) REFERENCES currencies (currencyid)
);
CREATE TABLE guests (
    guestid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    userid INT NOT NULL,
    FOREIGN KEY (userid) REFERENCES users (userid)
);
CREATE TABLE portfolios_guests (
    portfolioid INT NOT NULL,
    guestid INT NOT NULL,
    PRIMARY KEY (portfolioid, guestid),
    FOREIGN KEY (portfolioid) REFERENCES portfolios (portfolioid),
    FOREIGN KEY (guestid) REFERENCES guests (guestid)
);
CREATE TABLE bondcategories (
    bondcategoryid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    bondcategoryname VARCHAR(50) NOT NULL
);
CREATE TABLE bonds (
    bondid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    isin VARCHAR(50) NOT NULL UNIQUE,
    bonddescription VARCHAR(50),
    bondcategoryid INT NOT NULL,
    bondcurrencyid INT NOT NULL,
    FOREIGN KEY (bondcategoryid) REFERENCES bondcategories (bondcategoryid),
    FOREIGN KEY (bondcurrencyid) REFERENCES currencies (currencyid)
);
CREATE TABLE portfolios_bonds (
    portfolioid INT NOT NULL,
    bondid INT NOT NULL,
    quantity DECIMAL(12, 5) NOT NULL,
    PRIMARY KEY (portfolioid, bondid),
    FOREIGN KEY (portfolioid) REFERENCES portfolios (portfolioid),
    FOREIGN KEY (bondid) REFERENCES bonds (bondid)
);
CREATE TABLE bonddata (
    bonddataid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    bondid INT NOT NULL,
    rate DECIMAL(10, 5) NOT NULL,
    bonddatalogtime DATETIME NOT NULL,
    FOREIGN KEY (bondid) REFERENCES bonds (bondid),
    INDEX idx_bond_logtime (bondid, bonddatalogtime)
);
CREATE TABLE exchangerates (
    exchangerateid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    fromcurrencyid INT NOT NULL,
    tocurrencyid INT NOT NULL,
    rate DECIMAL(10, 5) NOT NULL,
    exchangeratelogtime DATETIME NOT NULL,
    FOREIGN KEY (fromcurrencyid) REFERENCES currencies (currencyid),
    FOREIGN KEY (tocurrencyid) REFERENCES currencies (currencyid),
    INDEX idx_fromcurrency_tocurrency_logtime (fromcurrencyid, tocurrencyid, exchangeratelogtime)
);