USE portfolioanalyzer;

CREATE PROCEDURE get_user_distinct_bond_isins(IN p_userid INT)
BEGIN
    SELECT DISTINCT b.bondid, b.bondsymbol
    FROM portfolio p
    JOIN portfolio_bond pb ON pb.portfolioid = p.portfolioid 
    JOIN bond b ON pb.bondid = b.bondid
    WHERE p.userid = p_userid;

END;