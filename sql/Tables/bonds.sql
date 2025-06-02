USE portfolioanalyzer;

CREATE TABLE bonds (
    bondid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    isin VARCHAR(50) NOT NULL UNIQUE,
    symbol VARCHAR(10) NOT NULL UNIQUE,
    bondname VARCHAR(50) NOT NULL,
    bonddescription VARCHAR(250),
    bondcategoryid INT NOT NULL,
    bondcurrencyid INT NOT NULL,
    FOREIGN KEY (bondcategoryid) REFERENCES bondcategories (bondcategoryid),
    FOREIGN KEY (bondcurrencyid) REFERENCES currencies (currencyid)
);