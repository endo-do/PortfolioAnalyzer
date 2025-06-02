USE portfolioanalyzer;

CREATE TABLE portfolios_bonds (
    portfolioid INT NOT NULL,
    bondid INT NOT NULL,
    quantity DECIMAL(15, 5) NOT NULL,
    PRIMARY KEY (portfolioid, bondid),
    FOREIGN KEY (portfolioid) REFERENCES portfolios (portfolioid),
    FOREIGN KEY (bondid) REFERENCES bonds (bondid)
);