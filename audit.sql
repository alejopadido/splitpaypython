DROP TABLE billing_audit;

CREATE TABLE billing_audit (
    audit_id      NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    bill_id       NUMBER NOT NULL,
    change_type   NVARCHAR2(50) NOT NULL, -- add, update, delete
    old_value     NVARCHAR2(1000), -- Optional, for logging previous values during modifications
    new_value     NVARCHAR2(1000), -- Optional, for logging new values during modifications
    changed_by    NVARCHAR2(200) NOT NULL, -- Username of the person making the change
    timestamp     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
