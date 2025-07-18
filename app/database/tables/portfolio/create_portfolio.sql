USE portfolioanalyzer;

CREATE TABLE portfolio (
    portfolioid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    userid INT NOT NULL,
    portfolioname VARCHAR(50) NOT NULL,
    portfoliodescription VARCHAR(255),
    portfoliocurrencyid INT NOT NULL,
    FOREIGN KEY (userid) REFERENCES user (userid) ON DELETE CASCADE,
    FOREIGN KEY (portfoliocurrencyid) REFERENCES currency (currencyid) ON DELETE RESTRICT
);