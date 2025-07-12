USE portfolioanalyzer;

CREATE TABLE exchangerate (
    exchangerateid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    fromcurrencyid INT NOT NULL,
    tocurrencyid INT NOT NULL,
    exchangerate DECIMAL(15, 5) NOT NULL,
    exchangeratelogtime DATE NOT NULL,
    FOREIGN KEY (fromcurrencyid) REFERENCES currency (currencyid),
    FOREIGN KEY (tocurrencyid) REFERENCES currency (currencyid),
    INDEX idx_fromcurrency_tocurrency_logtime (fromcurrencyid, tocurrencyid, exchangeratelogtime)
);