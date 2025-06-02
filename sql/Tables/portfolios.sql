USE portfolioanalyzer;

CREATE TABLE portfolios (
    portfolioid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    userid INT NOT NULL,
    portfolioname VARCHAR(50) NOT NULL,
    portfoliodescription VARCHAR(50),
    portfoliocurrencyid INT NOT NULL,
    FOREIGN KEY (userid) REFERENCES users (userid) ON DELETE CASCADE,
    FOREIGN KEY (portfoliocurrencyid) REFERENCES currencies (currencyid)
);