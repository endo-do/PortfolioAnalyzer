CREATE TABLE exchangerate (
    exchangerateid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    fromcurrencyid INT NOT NULL,
    tocurrencyid INT NOT NULL,
    exchangerate DECIMAL(15, 5) NOT NULL,
    exchangeratelogtime DATE NOT NULL,
    FOREIGN KEY (fromcurrencyid) REFERENCES currency (currencyid) ON DELETE CASCADE,
    FOREIGN KEY (tocurrencyid) REFERENCES currency (currencyid) ON DELETE CASCADE,
    INDEX idx_fromcurrency_tocurrency_logtime (fromcurrencyid, tocurrencyid, exchangeratelogtime)
);