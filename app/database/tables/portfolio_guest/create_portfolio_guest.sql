USE portfolioanalyzer;

CREATE TABLE portfolio_guest (
    portfolioid INT NOT NULL,
    userid INT NOT NULL,
    PRIMARY KEY (portfolioid, userid),
    FOREIGN KEY (portfolioid) REFERENCES portfolio (portfolioid),
    FOREIGN KEY (userid) REFERENCES user (userid)
);