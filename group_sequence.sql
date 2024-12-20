CREATE SEQUENCE group_seq
    START WITH 4
    INCREMENT BY 1
    NOCACHE;

SELECT MAX(groupid) FROM "Group";

DROP SEQUENCE GROUP_SEQ;

CREATE SEQUENCE GROUP_SEQ 
START WITH 4
INCREMENT BY 1 
NOCACHE;

ALTER TABLE transaction
ADD payment_method NVARCHAR2(20);

CREATE SEQUENCE transaction_seq 
    START WITH 1 
    INCREMENT BY 1;

ALTER TABLE transaction MODIFY groupid NULL;
ALTER TABLE transaction MODIFY BILLID NULL;

DESCRIBE transaction;

SELECT * FROM all_objects WHERE object_name = 'GET_USER_TOTAL_DEBT' AND object_type = 'FUNCTION';

SELECT get_user_total_debt(1) FROM dual;

SELECT table_name FROM all_tables WHERE owner = 'IS150403';
