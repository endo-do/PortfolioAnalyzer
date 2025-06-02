DROP DATABASE IF EXISTS portfolioanalyzer;
CREATE DATABASE portfolioanalyzer;

SOURCE ../Tables/users.sql;
SOURCE ../Tables/currencies.sql;
SOURCE ../Tables/portfolios.sql;
SOURCE ../Tables/portfolios_guests.sql;
SOURCE ../Tables/bondcategories.sql;
SOURCE ../Tables/bonds.sql;
SOURCE ../Tables/portfolios_bonds.sql;
SOURCE ../Tables/bonddata.sql;
SOURCE ../Tables/exchangerates.sql;

SOURCE ../Functions/get_bondcategory_value.sql;
SOURCE ../Functions/get_latest_exchangerate.sql;

SOURCE ../Procedures/read/get_distinct_user_bond_isins.sql;
SOURCE ../Procedures/read/get_user_portfolios.sql;

SOURCE ../Data/bondcategories.sql;
SOURCE ../Data/currencies.sql;