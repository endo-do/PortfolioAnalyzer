USE portfolioanalyzer;

CREATE TABLE bond (
    bondid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    bondsymbol VARCHAR(50) NOT NULL UNIQUE,
    bondname VARCHAR(50) NOT NULL,
    bonddescription TEXT,
    bondcountry VARCHAR(50),
    bondexchange INT,
    bondwebsite VARCHAR(100),
    bondindustry VARCHAR(50),
    bondsector VARCHAR(50),
    bondcategoryid INT NOT NULL,
    bondcurrencyid INT NOT NULL,
    FOREIGN KEY (bondcategoryid) REFERENCES bondcategory (bondcategoryid),
    FOREIGN KEY (bondcurrencyid) REFERENCES currency (currencyid) ON DELETE RESTRICT,
    FOREIGN KEY (bondexchange) REFERENCES exchange (exchangeid) ON DELETE RESTRICT
);