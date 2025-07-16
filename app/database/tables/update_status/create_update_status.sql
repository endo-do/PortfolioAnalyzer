USE portfolioanalyzer;

CREATE TABLE update_status (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    exchangerates DATE DEFAULT NULL,
    securities DATE DEFAULT NULL
);