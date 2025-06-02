USE portfolioanalyzer;

CREATE TABLE portfolios_guests (
    portfolioid INT NOT NULL,
    userid INT NOT NULL,
    PRIMARY KEY (portfolioid, userid),
    FOREIGN KEY (portfolioid) REFERENCES portfolios (portfolioid),
    FOREIGN KEY (userid) REFERENCES users (userid)
);