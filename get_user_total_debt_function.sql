CREATE OR REPLACE FUNCTION get_user_total_debt(p_userid IN NUMBER)
RETURN NUMBER
IS
    v_total_debt NUMBER := 0;
BEGIN
    SELECT SUM(b.amount * (ub.percentage / 100))
    INTO v_total_debt
    FROM user_bill ub
    JOIN bill b ON ub.billid = b.billid
    WHERE ub.userid = p_userid;

    RETURN NVL(v_total_debt, 0);
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN 0;
    WHEN OTHERS THEN
        RETURN -1; -- Indicating an error condition
END;
/
