CREATE OR REPLACE PROCEDURE add_user_to_group(
    p_userid IN NUMBER,
    p_groupid IN NUMBER,
    p_isleader IN CHAR
)
IS
BEGIN
    -- Insert the user into the user_group table with default values
    INSERT INTO user_group (userid, groupid, status, debt_status, isleader)
    VALUES (p_userid, p_groupid, 'active', 'No debt', p_isleader);

    DBMS_OUTPUT.PUT_LINE('User ' || p_userid || ' added to Group ' || p_groupid || ' successfully.');
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        DBMS_OUTPUT.PUT_LINE('User ' || p_userid || ' is already a member of Group ' || p_groupid);
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('An error occurred while adding User ' || p_userid || ' to Group ' || p_groupid);
END;
/
