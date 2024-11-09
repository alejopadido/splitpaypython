SELECT * 
FROM "User";

INSERT INTO "User" (USERID, NAME, EMAIL, PAYPALUSERNAME, PHONE)
VALUES (0, 'Alejandro', 'alejo@email.com', 'alejopaypal', '3186064342');

INSERT INTO "User" (USERID, NAME, EMAIL, PAYPALUSERNAME, PHONE)
VALUES (1, 'Sebastian', 'sebas@email.com', 'sebaspaypal', '3100000000');

commit;

-- DEMO INSERTS FOR TESTING PURPOSES
-- Insert sample data into "Group" table
INSERT INTO "Group" (groupid, name, createddate, status) VALUES 
(1, 'Finance Group', TO_DATE('2024-01-01', 'YYYY-MM-DD'), 'active');

INSERT INTO "Group" (groupid, name, createddate, status) VALUES 
(2, 'Travel Group', TO_DATE('2024-02-15', 'YYYY-MM-DD'), 'stopped');

INSERT INTO "Group" (groupid, name, createddate, status) VALUES 
(3, 'Study Group', TO_DATE('2024-03-10', 'YYYY-MM-DD'), 'ended');

-- Insert sample data into "User" table
INSERT INTO "User" (userid, name, email, paypalusername, phone) VALUES 
(3, 'Alice', 'alice@example.com', 'alice_paypal', '1234567890');

INSERT INTO "User" (userid, name, email, paypalusername, phone) VALUES 
(4, 'Bob', 'bob@example.com', 'bob_paypal', '0987654321');

INSERT INTO "User" (userid, name, email, paypalusername, phone) VALUES 
(5, 'Charlie', 'charlie@example.com', 'charlie_paypal', '1122334455');

-- Insert sample data into "bill" table
INSERT INTO bill (billid, title, amount, "date", status, location, receiptimage, groupid, type, comments) VALUES 
(1, 'Hotel Payment', 500, TO_DATE('2024-01-15', 'YYYY-MM-DD'), 'Pending', 'New York', NULL, 2, 'Lodging', 'Group trip expense');

INSERT INTO bill (billid, title, amount, "date", status, location, receiptimage, groupid, type, comments) VALUES 
(2, 'Dinner', 150, TO_DATE('2024-01-20', 'YYYY-MM-DD'), 'Approved', 'Los Angeles', NULL, 2, 'Food', 'Business dinner');

INSERT INTO bill (billid, title, amount, "date", status, location, receiptimage, groupid, type, comments) VALUES 
(3, 'Supplies', 80, TO_DATE('2024-02-10', 'YYYY-MM-DD'), 'Paid', NULL, NULL, 1, 'Office', 'Monthly office supplies');

-- Insert sample data into "notification" table
INSERT INTO notification (notificationid, type, message, "date", touserid) VALUES 
(1, 'E', 'Payment due', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 1);

INSERT INTO notification (notificationid, type, message, "date", touserid) VALUES 
(2, 'N', 'New bill available', TO_DATE('2024-01-20', 'YYYY-MM-DD'), 3);

INSERT INTO notification (notificationid, type, message, "date", touserid) VALUES 
(3, 'E', 'Reminder for meeting', TO_DATE('2024-02-05', 'YYYY-MM-DD'), 0);

-- Insert sample data into "transaction" table
INSERT INTO transaction (transactionid, amount, "date", description, payerid, payeeid, status, groupid, billid) VALUES 
(1, 500, TO_DATE('2024-01-15', 'YYYY-MM-DD'), 'Hotel reimbursement', 1, 0, 'approved', 2, 1);

INSERT INTO transaction (transactionid, amount, "date", description, payerid, payeeid, status, groupid, billid) VALUES 
(2, 150, TO_DATE('2024-01-20', 'YYYY-MM-DD'), 'Dinner reimbursement', 0, 1, 'pending', 2, 2);

INSERT INTO transaction (transactionid, amount, "date", description, payerid, payeeid, status, groupid, billid) VALUES 
(3, 80, TO_DATE('2024-02-10', 'YYYY-MM-DD'), 'Supplies reimbursement', 3, 1, 'approved', 1, 3);

-- Insert sample data into "user_bill" table
INSERT INTO user_bill (userid, billid) VALUES 
(1, 1);

INSERT INTO user_bill (userid, billid) VALUES 
(0, 2);

INSERT INTO user_bill (userid, billid) VALUES 
(3, 3);

-- Insert sample data into "user_group" table
INSERT INTO user_group (userid, groupid, status, debt_status, isleader) VALUES 
(1, 1, 'active', 'No debt', 'Y');

INSERT INTO user_group (userid, groupid, status, debt_status, isleader) VALUES 
(0, 2, 'active', 'Indebted', 'N');

INSERT INTO user_group (userid, groupid, status, debt_status, isleader) VALUES 
(3, 3, 'offline', 'Paid', 'N');

-- Query Testing

SELECT g.groupid, g.name, g.createddate, g.status
FROM "User" u
JOIN user_group ug ON u.userid = ug.userid
JOIN "Group" g ON ug.groupid = g.groupid
WHERE u.name = :username;

