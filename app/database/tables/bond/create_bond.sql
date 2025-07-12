USE portfolioanalyzer;

CREATE TABLE bond (
    bondid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    isin VARCHAR(50) NOT NULL UNIQUE,
    bondsymbol VARCHAR(50) NOT NULL UNIQUE,
    bondname VARCHAR(50) NOT NULL,
    bonddescription VARCHAR(250),
    bondcategoryid INT NOT NULL,
    bondcurrencyid INT NOT NULL,
    FOREIGN KEY (bondcategoryid) REFERENCES bondcategory (bondcategoryid),
    FOREIGN KEY (bondcurrencyid) REFERENCES currency (currencyid)
);