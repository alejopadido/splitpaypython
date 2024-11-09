SELECT * 
FROM "User";

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
