CREATE TABLE bond (
    bondid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    bondsymbol VARCHAR(50) NOT NULL UNIQUE,
    bondname VARCHAR(50) NOT NULL,
    bonddescription TEXT,
    bondcountry VARCHAR(50),
    bondexchangeid INT,
    bondwebsite VARCHAR(100),
    bondindustry VARCHAR(50),
    bondsectorid INT,
    bondcategoryid INT NOT NULL,
    bondcurrencyid INT NOT NULL,
    FOREIGN KEY (bondcategoryid) REFERENCES bondcategory (bondcategoryid),
    FOREIGN KEY (bondcurrencyid) REFERENCES currency (currencyid) ON DELETE RESTRICT,
    FOREIGN KEY (bondexchangeid) REFERENCES exchange (exchangeid) ON DELETE RESTRICT,
    FOREIGN KEY (bondsectorid) REFERENCES sector (sectorid) ON DELETE RESTRICT
);