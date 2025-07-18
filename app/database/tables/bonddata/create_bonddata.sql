USE portfolioanalyzer;

CREATE TABLE bonddata (
    bonddataid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    bondid INT NOT NULL,
    bondrate DECIMAL(15, 5) NOT NULL,
    bonddatalogtime DATE NOT NULL,
    FOREIGN KEY (bondid) REFERENCES bond (bondid) ON DELETE CASCADE,
    INDEX idx_bond_logtime (bondid, bonddatalogtime)
);