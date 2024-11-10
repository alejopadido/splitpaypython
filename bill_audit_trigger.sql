CREATE OR REPLACE TRIGGER bill_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON bill
FOR EACH ROW
DECLARE
    v_old_value NVARCHAR2(4000);
    v_new_value NVARCHAR2(4000);
BEGIN
    -- Handling INSERT operations
    IF INSERTING THEN
        v_new_value := 'Title: ' || :NEW.title || ', Amount: ' || TO_CHAR(:NEW.amount) || 
                       ', Date: ' || TO_CHAR(:NEW."date", 'YYYY-MM-DD') || ', Status: ' || :NEW.status || 
                       ', Location: ' || :NEW.location || ', Group ID: ' || TO_CHAR(:NEW.groupid) || 
                       ', Type: ' || :NEW.type || ', Comments: ' || :NEW.comments;

        INSERT INTO billing_audit (bill_id, change_type, new_value, changed_by, timestamp)
        VALUES (:NEW.billid, 'add', v_new_value, USER, SYSTIMESTAMP);

    -- Handling UPDATE operations
    ELSIF UPDATING THEN
        v_old_value := 'Title: ' || :OLD.title || ', Amount: ' || TO_CHAR(:OLD.amount) || 
                       ', Date: ' || TO_CHAR(:OLD."date", 'YYYY-MM-DD') || ', Status: ' || :OLD.status || 
                       ', Location: ' || :OLD.location || ', Group ID: ' || TO_CHAR(:OLD.groupid) || 
                       ', Type: ' || :OLD.type || ', Comments: ' || :OLD.comments;

        v_new_value := 'Title: ' || :NEW.title || ', Amount: ' || TO_CHAR(:NEW.amount) || 
                       ', Date: ' || TO_CHAR(:NEW."date", 'YYYY-MM-DD') || ', Status: ' || :NEW.status || 
                       ', Location: ' || :NEW.location || ', Group ID: ' || TO_CHAR(:NEW.groupid) || 
                       ', Type: ' || :NEW.type || ', Comments: ' || :NEW.comments;

        INSERT INTO billing_audit (bill_id, change_type, old_value, new_value, changed_by, timestamp)
        VALUES (:NEW.billid, 'update', v_old_value, v_new_value, USER, SYSTIMESTAMP);

    -- Handling DELETE operations
    ELSIF DELETING THEN
        v_old_value := 'Title: ' || :OLD.title || ', Amount: ' || TO_CHAR(:OLD.amount) || 
                       ', Date: ' || TO_CHAR(:OLD."date", 'YYYY-MM-DD') || ', Status: ' || :OLD.status || 
                       ', Location: ' || :OLD.location || ', Group ID: ' || TO_CHAR(:OLD.groupid) || 
                       ', Type: ' || :OLD.type || ', Comments: ' || :OLD.comments;

        INSERT INTO billing_audit (bill_id, change_type, old_value, changed_by, timestamp)
        VALUES (:OLD.billid, 'delete', v_old_value, USER, SYSTIMESTAMP);
    END IF;
END;
/
commit;