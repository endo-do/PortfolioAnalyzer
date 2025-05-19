USE portfolioanalyser;

-- 1 User
INSERT INTO users (username, userpwd) VALUES ('testuser', 'passwordhash');

-- 3 Currencies
INSERT INTO currencies (currencyname) VALUES ('CHF'), ('EUR'), ('USD');

-- 1 Portfolio für User 1 mit CHF als Portfolio-Währung (currencyid 1)
INSERT INTO portfolios (userid, portfoliodescription, portfoliocurrencyid) VALUES (1, 'Mein Portfolio', 1);

-- 1 Bond-Kategorie
INSERT INTO bondcategories (bondcategoryname) VALUES ('Staatsanleihe');
INSERT INTO bondcategories (bondcategoryname) VALUES ('Aktie');

-- 5 Bonds mit unterschiedlichen ISINs, alle in CHF (currencyid = 1) und Kategorie 1
INSERT INTO bonds (isin, bonddescription, bondcategoryid, bondcurrencyid) VALUES
('CH000000001', 'Bond 1', 1, 1),
('CH000000002', 'Bond 2', 1, 1),
('CH000000003', 'Bond 3', 1, 1),
('CH000000004', 'Bond 4', 1, 1),
('CH000000005', 'Bond 5', 1, 1);

-- 5 Bonds in Portfolio 1 mit Mengen von 1 bis 10
INSERT INTO portfolios_bonds (portfolioid, bondid, quantity) VALUES
(1, 1, 1),
(1, 2, 2),
(1, 3, 5),
(1, 4, 7),
(1, 5, 10);

-- Bonddata mit Kursen von 5 bis 500 (jeweils aktuelles Datum)
INSERT INTO bonddata (bondid, bondrate, bonddatalogtime) VALUES
(1, 5.00, NOW()),
(2, 50.00, NOW()),
(3, 100.00, NOW()),
(4, 250.00, NOW()),
(5, 500.00, NOW());

INSERT INTO exchangerates (fromcurrencyid, tocurrencyid, exchangerate, exchangeratelogtime) VALUES
(1, 1, 1, NOW()),
(2, 1, 0.95, NOW()),  -- EUR -> CHF
(3, 1, 0.90, NOW());  -- USD -> CHF