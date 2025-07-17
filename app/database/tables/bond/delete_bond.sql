USE portfolioanalyzer;

CREATE PROCEDURE delete_bond(IN in_bond_id INT)
BEGIN
    DELETE FROM portfolio_bond WHERE bondid = in_bond_id;
    DELETE FROM bonddata WHERE bondid = in_bond_id;
    DELETE FROM bond WHERE bondid = in_bond_id;
END;