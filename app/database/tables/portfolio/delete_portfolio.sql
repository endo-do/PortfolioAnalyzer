USE portfolioanalyzer;

CREATE PROCEDURE delete_portfolio(IN in_portfolio_id INT)
BEGIN
    DELETE FROM portfolio_bond WHERE portfolioid = in_portfolio_id;
    DELETE FROM portfolio WHERE portfolioid = in_portfolio_id;
END;