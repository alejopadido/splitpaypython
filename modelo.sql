-- Generado por Oracle SQL Developer Data Modeler 23.1.0.087.0806
--   en:        2024-11-05 07:14:33 COT
--   sitio:      Oracle Database 11g
--   tipo:      Oracle Database 11g



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
    billid NUMBER NOT NULL
);

ALTER TABLE user_bill ADD CONSTRAINT user_bill_pk PRIMARY KEY ( userid,
                                                                billid );

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



-- Informe de Resumen de Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                             7
-- CREATE INDEX                             0
-- ALTER TABLE                             22
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   1
-- WARNINGS                                 1