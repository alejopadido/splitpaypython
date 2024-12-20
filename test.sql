SELECT * 
FROM "User";

SELECT * FROM user_group;

SELECT * FROM bill;
-- Query Testing

SELECT g.groupid, g.name, g.createddate, g.status
FROM "User" u
JOIN user_group ug ON u.userid = ug.userid
JOIN "Group" g ON ug.groupid = g.groupid
WHERE u.name = :username;

SELECT u.name,
       SUM(b.amount * (ub.percentage / 100)) AS total_debt
FROM user_bill ub
JOIN bill b ON ub.billid = b.billid
JOIN "User" u ON ub.userid = u.userid
WHERE b.groupid = :group_id
GROUP BY u.name, b.groupid;

-- Gets the deb status of each user in a determined group, name, groupId, totalDebt, totalPaid, paymentStatus, percentagePaid
WITH user_total_debt AS (
    SELECT u.userid,
           u.name,
           b.groupid,
           SUM(b.amount * (ub.percentage / 100)) AS total_debt
    FROM user_bill ub
    JOIN bill b ON ub.billid = b.billid
    JOIN "User" u ON ub.userid = u.userid
    WHERE b.groupid = :group_id
    GROUP BY u.userid, u.name, b.groupid
),
user_total_paid AS (
    SELECT t.payerid AS userid,
           b.groupid,
           SUM(t.amount) AS total_paid
    FROM transaction t
    JOIN bill b ON t.billid = b.billid
    WHERE t.status = 'approved' AND b.groupid = :group_id
    GROUP BY t.payerid, b.groupid
)
SELECT utd.name,
       utd.groupid,
       utd.total_debt,
       NVL(utp.total_paid, 0) AS total_paid,
       CASE 
           WHEN NVL(utp.total_paid, 0) >= utd.total_debt THEN 'Paid'
           ELSE 'Indebted'
       END AS payment_status,
       ROUND((NVL(utp.total_paid, 0) / utd.total_debt) * 100, 2) AS percentage_paid
FROM user_total_debt utd
LEFT JOIN user_total_paid utp ON utd.userid = utp.userid AND utd.groupid = utp.groupid;

-- CRUD Operations for Trigger testing
INSERT INTO bill (title, amount, "date", status, location, groupid, type, comments)
VALUES ('Test Bill', 100, TO_DATE('2024-12-01', 'YYYY-MM-DD'), 'Pending', 'New York', 1, 'Business', 'Initial bill for testing');
commit;

UPDATE bill
SET amount = 150, status = 'Approved'
WHERE title = 'Test Bill';
commit;

-- Audit table
SELECT * FROM billing_audit ORDER BY timestamp DESC;

-----------query testing sebas ------------
SELECT TO_CHAR(b."date", 'YYYY-Month') AS Bill_Month,
       SUM(b.amount) AS Total
FROM BILL b
GROUP BY TO_CHAR(b."date", 'YYYY-Month')
ORDER BY Bill_Month;


-------t1
 SELECT TO_CHAR(b."date", 'YYYY-Month') AS Bill_Month,
               NVL(SUM(CASE WHEN g.groupid = 1 THEN b.amount END), 0) AS "Group 1",
               NVL(SUM(CASE WHEN g.groupid = 2 THEN b.amount END), 0) AS "Group 2",
               -- Add more cases if there are more groups dynamically
               NVL(SUM(b.amount), 0) AS "Total"
        FROM "IS150403"."BILL" b
        JOIN "IS150403"."USER_GROUP" ug ON b.groupid = ug.groupid
        JOIN "IS150403"."GROUP" g ON ug.groupid = g.groupid
        GROUP BY TO_CHAR(b."date", 'YYYY-Month')
        ORDER BY Bill_Month;



-------t2
SELECT TO_CHAR(b."date", 'YYYY-Month') AS Bill_Month,
               NVL(SUM(CASE WHEN g.groupid = 1 THEN b.amount END), 0) AS "Group 1",
               NVL(SUM(CASE WHEN g.groupid = 2 THEN b.amount END), 0) AS "Group 2",
               NVL(SUM(b.amount), 0) AS "Total"
        FROM "IS150403"."BILL" b
        JOIN "IS150403"."USER_GROUP" ug ON b.groupid = ug.groupid
        JOIN "IS150403"."GROUP" g ON ug.groupid = g.groupid
        GROUP BY TO_CHAR(b."date", 'YYYY-Month')
        ORDER BY Bill_Month;

-- testing tables
SELECT * FROM "IS150403"."BILL" WHERE ROWNUM = 1;
SELECT * FROM "IS150403"."USER_GROUP" WHERE ROWNUM = 1;
SELECT * FROM "IS150403"."GROUP" WHERE ROWNUM = 1;

--gradual

SELECT TO_CHAR(b."date", 'YYYY-Month') AS Bill_Month,
       SUM(b.amount) AS Total
FROM "IS150403"."BILL" b
GROUP BY TO_CHAR(b."date", 'YYYY-Month')
ORDER BY Bill_Month;

--gradual 2
SELECT TO_CHAR(b."date", 'YYYY-Month') AS Bill_Month,
       SUM(b.amount) AS Total
FROM "IS150403"."BILL" b
JOIN "IS150403"."USER_GROUP" ug ON b.groupid = ug.groupid
GROUP BY TO_CHAR(b."date", 'YYYY-Month')
ORDER BY Bill_Month;

--gradual 3
SELECT TO_CHAR(b."date", 'YYYY-Month') AS Bill_Month,
       NVL(SUM(CASE WHEN g.groupid = 1 THEN b.amount END), 0) AS "Group 1",
       NVL(SUM(CASE WHEN g.groupid = 2 THEN b.amount END), 0) AS "Group 2",
       SUM(b.amount) AS Total
FROM "IS150403"."BILL" b
JOIN "IS150403"."USER_GROUP" ug ON b.groupid = ug.groupid
JOIN "IS150403"."Group" g ON ug.groupid = g.groupid
GROUP BY TO_CHAR(b."date", 'YYYY-Month')
ORDER BY Bill_Month;

SELECT * FROM all_tables WHERE table_name = 'Group';
