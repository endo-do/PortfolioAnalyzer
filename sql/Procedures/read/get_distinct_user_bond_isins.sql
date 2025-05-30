USE portfolioanalyzer;

DELIMITER //

CREATE PROCEDURE get_user_distinct_bond_isins(IN p_userid INT)
BEGIN
    SELECT DISTINCT b.bondid, b.symbol
    FROM portfolios p
    JOIN portfolios_bonds pb ON pb.portfolioid = p.portfolioid 
    JOIN bonds b ON pb.bondid = b.bondid
    WHERE p.userid = p_userid;

END //

DELIMITER;