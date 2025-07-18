USE portfolioanalyzer;

CREATE TABLE portfolio_bond (
    portfolioid INT NOT NULL,
    bondid INT NOT NULL,
    quantity DECIMAL(15, 5) NOT NULL,
    PRIMARY KEY (portfolioid, bondid),
    FOREIGN KEY (portfolioid) REFERENCES portfolio (portfolioid) ON DELETE CASCADE,
    FOREIGN KEY (bondid) REFERENCES bond (bondid) ON DELETE CASCADE
);