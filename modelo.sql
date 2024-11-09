DROP TABLE bill CASCADE CONSTRAINTS;

DROP TABLE "Group" CASCADE CONSTRAINTS;

DROP TABLE notification CASCADE CONSTRAINTS;

DROP TABLE transaction CASCADE CONSTRAINTS;

DROP TABLE "User" CASCADE CONSTRAINTS;

DROP TABLE user_bill CASCADE CONSTRAINTS;

DROP TABLE user_group CASCADE CONSTRAINTS;

-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE bill (
    billid       NUMBER NOT NULL,
    title        NVARCHAR2(200) NOT NULL,
    amount       NUMBER NOT NULL,
    "date"       DATE NOT NULL,
    status       NVARCHAR2(10) NOT NULL,
    location     NVARCHAR2(200),
    receiptimage BLOB,
    groupid      NUMBER NOT NULL,
    type         NVARCHAR2(100),
    comments     NVARCHAR2(300)
);

ALTER TABLE bill ADD constraint bill_status 
    CHECK (status in ('Pending', 'Approved', 'Debt', 'Paid'))
;
ALTER TABLE bill ADD CONSTRAINT bill_pk PRIMARY KEY ( billid );

CREATE TABLE "Group" (
    groupid     NUMBER NOT NULL,
    name        NVARCHAR2(200) NOT NULL,
    createddate DATE NOT NULL,
    status      NVARCHAR2(10) NOT NULL
);

-- Error - Index Group__IDX has no columns

ALTER TABLE "Group" ADD constraint group_status 
    CHECK (status in ('active', 'stopped', 'ended'))
;
ALTER TABLE "Group" ADD CONSTRAINT group_pk PRIMARY KEY ( groupid );

CREATE TABLE notification (
    notificationid NUMBER NOT NULL,
    type           CHAR 
--  WARNING: CHAR size not specified 
     NOT NULL,
    message        NVARCHAR2(1000) NOT NULL,
    "date"         DATE NOT NULL,
    touserid       NUMBER NOT NULL
);

COMMENT ON COLUMN notification.type IS
    '''E'' Email
''N'' Push Notification';

ALTER TABLE notification ADD CONSTRAINT notification_pk PRIMARY KEY ( notificationid );

CREATE TABLE transaction (
    transactionid NUMBER NOT NULL,
    amount        NUMBER NOT NULL,
    "date"        DATE NOT NULL,
    description   NVARCHAR2(300),
    payerid       NUMBER NOT NULL,
    payeeid       NUMBER NOT NULL,
    status        NVARCHAR2(10) NOT NULL,
    groupid       NUMBER NOT NULL,
    billid        NUMBER NOT NULL
);

ALTER TABLE transaction ADD constraint transaction_status 
    CHECK (status in ('approved', 'pending'))
;
ALTER TABLE transaction ADD CONSTRAINT transaction_pk PRIMARY KEY ( transactionid );

CREATE TABLE "User" (
    userid         NUMBER NOT NULL,
    name           NVARCHAR2(200) NOT NULL,
    email          NVARCHAR2(200) NOT NULL,
    paypalusername NVARCHAR2(200) NOT NULL,
    phone          NVARCHAR2(200) NOT NULL
);

ALTER TABLE "User" ADD CONSTRAINT user_pk PRIMARY KEY ( userid );

CREATE TABLE user_bill (
    userid NUMBER NOT NULL,
    billid NUMBER NOT NULL,
    percentage NUMBER NOT NULL
);

ALTER TABLE user_bill ADD CONSTRAINT user_bill_pk PRIMARY KEY (userid, billid);

-- Constraint to ensure the percentage is between 0 and 100
ALTER TABLE user_bill ADD CONSTRAINT user_bill_percentage_chk
    CHECK (percentage >= 0 AND percentage <= 100);



CREATE TABLE user_group (
    userid      NUMBER NOT NULL,
    groupid     NUMBER NOT NULL,
    status      NVARCHAR2(10) NOT NULL,
    debt_status NVARCHAR2(10) NOT NULL,
    isleader    CHAR(1) NOT NULL
);

ALTER TABLE user_group ADD constraint user_group_status 
    CHECK (status in ('offline', 'active', 'pending'))
;

ALTER TABLE User_Group 
    ADD CONSTRAINT User_Group_debt_status 
    CHECK (debt_status in ('Paid', 'Indebted', 'No debt'))
;
ALTER TABLE user_group ADD CONSTRAINT user_group_pk PRIMARY KEY ( userid,
                                                                  groupid );

ALTER TABLE bill
    ADD CONSTRAINT bill_group_fk FOREIGN KEY ( groupid )
        REFERENCES "Group" ( groupid );

ALTER TABLE notification
    ADD CONSTRAINT notification_user_fk FOREIGN KEY ( touserid )
        REFERENCES "User" ( userid );

ALTER TABLE transaction
    ADD CONSTRAINT transaction_bill_fk FOREIGN KEY ( billid )
        REFERENCES bill ( billid );

ALTER TABLE transaction
    ADD CONSTRAINT transaction_group_fk FOREIGN KEY ( groupid )
        REFERENCES "Group" ( groupid );

ALTER TABLE transaction
    ADD CONSTRAINT transaction_user_fk FOREIGN KEY ( payerid )
        REFERENCES "User" ( userid );

ALTER TABLE transaction
    ADD CONSTRAINT transaction_user_fkv2 FOREIGN KEY ( payeeid )
        REFERENCES "User" ( userid );

ALTER TABLE user_bill
    ADD CONSTRAINT user_bill_bill_fk FOREIGN KEY ( billid )
        REFERENCES bill ( billid );

ALTER TABLE user_bill
    ADD CONSTRAINT user_bill_user_fk FOREIGN KEY ( userid )
        REFERENCES "User" ( userid );

ALTER TABLE user_group
    ADD CONSTRAINT user_group_group_fk FOREIGN KEY ( groupid )
        REFERENCES "Group" ( groupid );

ALTER TABLE user_group
    ADD CONSTRAINT user_group_user_fk FOREIGN KEY ( userid )
        REFERENCES "User" ( userid );


-- INSERTS
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
-- Insert sample data into "user_bill" table
INSERT INTO user_bill (userid, billid, percentage) VALUES (1, 1, 50);  -- User 1 owes 50% of Bill 1
INSERT INTO user_bill (userid, billid, percentage) VALUES (0, 2, 100); -- User 0 owes 100% of Bill 2
INSERT INTO user_bill (userid, billid, percentage) VALUES (3, 3, 25);  -- User 3 owes 25% of Bill 3

-- Insert sample data into "user_group" table
INSERT INTO user_group (userid, groupid, status, debt_status, isleader) VALUES 
(1, 1, 'active', 'No debt', 'Y');

INSERT INTO user_group (userid, groupid, status, debt_status, isleader) VALUES 
(0, 2, 'active', 'Indebted', 'N');

INSERT INTO user_group (userid, groupid, status, debt_status, isleader) VALUES 
(3, 3, 'offline', 'Paid', 'N');