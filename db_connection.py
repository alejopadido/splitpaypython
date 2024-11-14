import os
import cx_Oracle

# Add Oracle Instant Client path to environment variable
#os.environ["PATH"] = r"C:\Users\alejo\dev\instantclient_23_6;" + os.environ["PATH"] #Alejo
os.environ["PATH"] = r"D:\sebastian\DESARROLLO\instantclient_23_6;" + os.environ["PATH"] #Sebas


# Database connection settings
HOST = "orion.javeriana.edu.co"
PORT = "1521"
SERVICE_NAME = "LAB"
USER = "is150403"
PASSWORD = "eTvw97#g#qyrift"

# Connect to db
def get_connection():
    """
    Establish and return a database connection using cx_Oracle.
    """
    dsn = cx_Oracle.makedsn(HOST, PORT, service_name=SERVICE_NAME)
    connection = cx_Oracle.connect(user=USER, password=PASSWORD, dsn=dsn)   
    # if connection != None: print('Connection successful!')
    return connection

# Check if a user exists in the db
def check_user_exists(username, email, phone):
    print('Username: ' + username + " Email: " + email + " Phone: " + phone)

    connection = None
    try:
        # Establish the database connection
        connection = get_connection()
        cursor = connection.cursor()

        # Query to check if the user exists
        query = """
            SELECT * FROM "IS150403"."User"
            WHERE name = :username AND email = :email AND phone = :phone
        """
        # Execute the query using parameterized input
        cursor.execute(query, {"username": username, "email": email, "phone": phone})
        
        result = cursor.fetchone()
        return result is not None

    except cx_Oracle.DatabaseError as e:
        # Log or handle the database error
        print("Database error:", e)
        return False

    finally:
        # Close the connection if it was established
        if connection:
            connection.close()

# Get user groups
def get_user_groups(username):
    connection = None
    try:
        # Establish the database connection
        connection = get_connection()
        cursor = connection.cursor()

        # Query to get the list of groups for the given username
        query = """
            SELECT g.groupid, g.name, g.createddate, g.status
            FROM "IS150403"."User" u
            JOIN "IS150403".user_group ug ON u.userid = ug.userid
            JOIN "IS150403"."Group" g ON ug.groupid = g.groupid
            WHERE u.name = :username
        """

        # Execute the query using parameterized input
        cursor.execute(query, {"username": username})

        # Fetch all results
        groups = cursor.fetchall()

        # Return the list of groups (each item is a tuple)
        return groups

    except cx_Oracle.DatabaseError as e:
        # Log or handle the database error
        print("Database error:", e)
        return []

    finally:
        # Close the connection if it was established
        if connection:
            connection.close()

# Get all the members of a group
def get_group_members(group_id):
    """
    Get the list of members of a specific group by group_id.
    Returns a list of members (user ID, name, email).
    """
    connection = None
    try:
        # Establish the database connection
        connection = get_connection()
        cursor = connection.cursor()

        # Query to get the list of members for the given group_id
        query = """
            SELECT u.userid, u.name, u.email
            FROM "IS150403"."User" u
            JOIN "IS150403".user_group ug ON u.userid = ug.userid
            WHERE ug.groupid = :group_id
        """

        # Execute the query using parameterized input
        cursor.execute(query, {"group_id": group_id})

        # Fetch all results
        members = cursor.fetchall()

        # Return the list of members (each item is a tuple)
        return members

    except cx_Oracle.DatabaseError as e:
        # Log or handle the database error
        print("Database error:", e)
        return []

    finally:
        # Close the connection if it was established
        if connection:
            connection.close()

# Gets each group member debt information
def get_group_member_debts(group_id):
    """
    Get the list of members of a specific group and their debt details.
    Returns a list of members with their name, total debt, total paid, payment status, and percentage paid.
    """
    connection = None
    try:
        # Establish the database connection
        connection = get_connection()
        cursor = connection.cursor()

        # Query to get the financial details of the members of the group
        query = """
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
               utd.total_debt,
               NVL(utp.total_paid, 0) AS total_paid,
               CASE 
                   WHEN NVL(utp.total_paid, 0) >= utd.total_debt THEN 'Paid'
                   ELSE 'Indebted'
               END AS payment_status,
               ROUND((NVL(utp.total_paid, 0) / utd.total_debt) * 100, 2) AS percentage_paid
        FROM user_total_debt utd
        LEFT JOIN user_total_paid utp ON utd.userid = utp.userid AND utd.groupid = utp.groupid
        """

        # Execute the query using parameterized input
        cursor.execute(query, {"group_id": group_id})

        # Fetch all results
        members_debts = cursor.fetchall()

        # Return the list of members' debt details (each item is a tuple)
        return members_debts

    except cx_Oracle.DatabaseError as e:
        # Log or handle the database error
        print("Database error:", e)
        return []

    finally:
        # Close the connection if it was established
        if connection:
            connection.close()

# Creates a new bill
def add_bill(title, amount, bill_date, status, location, group_id, bill_type, comments):
    """
    Adds a new bill to the bill table and returns the new bill ID.
    """
    connection = None
    try:
        # Establish the database connection
        connection = get_connection()
        cursor = connection.cursor()

        # Insert new bill (billid will be auto-generated)
        query = """
            INSERT INTO bill (title, amount, "date", status, location, groupid, type, comments)
            VALUES (:title, :amount, TO_DATE(:bill_date, 'YYYY-MM-DD'), :status, :location, :group_id, :bill_type, :comments)
            RETURNING billid INTO :billid
        """
        # Define the variable to capture the generated bill ID
        bill_id_var = cursor.var(cx_Oracle.NUMBER)
        # Execute the insert query
        cursor.execute(query, {
            "title": title,
            "amount": amount,
            "bill_date": bill_date,
            "status": status,
            "location": location,
            "group_id": group_id,
            "bill_type": bill_type,
            "comments": comments,
            "billid": bill_id_var
        })
        connection.commit()

        # Return the generated bill ID
        return bill_id_var.getvalue()[0]

    except cx_Oracle.DatabaseError as e:
        print("Database error:", e)
        return None

    finally:
        if connection:
            connection.close()

# Creates the relation between a user and a bill
def add_user_bill(userid, billid, percentage):
    """
    Adds a user-bill assignment to the user_bill table.
    """
    connection = None
    try:
        # Establish the database connection
        connection = get_connection()
        cursor = connection.cursor()

        # Insert user bill assignment
        query = """
            INSERT INTO user_bill (userid, billid, percentage)
            VALUES (:userid, :billid, :percentage)
        """
        cursor.execute(query, {"userid": userid, "billid": billid, "percentage": percentage})
        connection.commit()
        print(f"Successfully added user {userid} to bill {billid} with {percentage}% responsibility.")

    except cx_Oracle.DatabaseError as e:
        print("Database error:", e)

    finally:
        if connection:
            connection.close()

# Function to create a new group
def create_group(group_name, created_by_userid):
    """
    Creates a new group in the Group table.
    Returns the group ID of the created group.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Insert new group into Group table
        query = """
            INSERT INTO "Group" (groupid, name, createddate, status)
            VALUES (GROUP_SEQ.NEXTVAL, :group_name, SYSDATE, 'active')
            RETURNING groupid INTO :group_id
        """
        group_id_var = cursor.var(cx_Oracle.NUMBER)
        cursor.execute(query, {"group_name": group_name, "group_id": group_id_var})
        connection.commit()

        # Retrieve the generated group ID
        group_id = group_id_var.getvalue()[0]

        # Assign the creating user as the group leader in the user_group table
        cursor.execute("""
            INSERT INTO user_group (userid, groupid, status, debt_status, isleader)
            VALUES (:user_id, :group_id, 'active', 'No debt', 'Y')
        """, {"user_id": created_by_userid, "group_id": group_id})
        connection.commit()

       # print(f"Group '{group_name}' created successfully with Group ID: {group_id}")
        return group_id

    except cx_Oracle.DatabaseError as e:
        print("Database error:", e)
        return None

    finally:
        if connection:
            connection.close()

# Function to add a user to an existing group
def add_user_to_group(user_id, group_id, is_leader='N'):
    """
    Adds a user to an existing group in the user_group table.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Insert user into user_group relationship
        query = """
            INSERT INTO user_group (userid, groupid, status, debt_status, isleader)
            VALUES (:user_id, :group_id, 'active', 'No debt', :is_leader)
        """
        cursor.execute(query, {"user_id": user_id, "group_id": group_id, "is_leader": is_leader})
        connection.commit()

        print(f"User {user_id} added to group {group_id} successfully.")

    except cx_Oracle.DatabaseError as e:
        print("Database error:", e)

    finally:
        if connection:
            connection.close()

def member_to_member_transaction(from_user_id, to_user_id, amount, clear_debt, payment_method, billId, group_id=None):
    """
    Handles a transaction between two users.
    :param from_user_id: The ID of the payer.
    :param to_user_id: The ID of the payee.
    :param amount: The amount to be transferred.
    :param clear_debt: Boolean indicating whether to clear all debt.
    :param payment_method: The selected payment method (PayPal or Cash).
    :param group_id: The ID of the group (optional).
    :param billId: ID of the bill.
    :return: Boolean indicating success or failure of the transaction.
    """
    connection = None
    try:
        # Establish the database connection
        connection = get_connection()
        cursor = connection.cursor()

        # If clear_debt is True, calculate the total outstanding debt using the PL/SQL function
        if clear_debt:
            total_debt = cursor.callfunc('GET_USER_TOTAL_DEBT', cx_Oracle.NUMBER, [from_user_id])
            amount = total_debt if total_debt > 0 else amount

        # Insert the transaction into the transaction table, including group_id if provided
        query = """
            INSERT INTO transaction (transactionid, amount, "date", description, payerid, payeeid, status, payment_method, groupid, billid)
            VALUES (transaction_seq.NEXTVAL, :amount, SYSDATE, :description, :from_user_id, :to_user_id, 'approved', :payment_method, :group_id, :billId)
        """
        description = f"Payment from User ID {from_user_id} to User ID {to_user_id} via {payment_method}"
        cursor.execute(query, {
            "amount": amount,
            "description": description,
            "from_user_id": from_user_id,
            "to_user_id": to_user_id,
            "payment_method": payment_method,
            "group_id": group_id,  # This will be None if not provided
            "billId": billId
        })

        # If clear_debt is True, update the status of the pending debts to "approved"
        if clear_debt and total_debt > 0:
            cursor.execute("""
                UPDATE transaction 
                SET status = 'approved'
                WHERE payerid = :from_user_id AND payeeid = :to_user_id AND status = 'pending'
            """, {"from_user_id": from_user_id, "to_user_id": to_user_id})
            print("All debt cleared.")

        # Commit the transaction
        connection.commit()
        print(f"Transaction of {amount} from User ID {from_user_id} to User ID {to_user_id} via {payment_method} was successful.")
        return True

    except cx_Oracle.DatabaseError as e:
        print("Database error:", e)
        return False

    finally:
        if connection:
            connection.close()

def get_bill_report():
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Execute the report query
        query = """
        SELECT TO_CHAR(b."date", 'YYYY-Month') AS Bill_Month,
               NVL(SUM(CASE WHEN g.groupid = 1 THEN b.amount END), 0) AS "Group 1",
               NVL(SUM(CASE WHEN g.groupid = 2 THEN b.amount END), 0) AS "Group 2",
               -- Add more cases if there are more groups dynamically
               NVL(SUM(b.amount), 0) AS "Total"
        FROM "IS150403"."BILL" b
        JOIN "IS150403"."USER_GROUP" ug ON b.groupid = ug.groupid
        JOIN "IS150403"."Group" g ON ug.groupid = g.groupid
        GROUP BY TO_CHAR(b."date", 'YYYY-Month')
        ORDER BY Bill_Month
        """

        cursor.execute(query)
        report_data = cursor.fetchall()

        # Print the report in table format
        print("Report by Date and Group:")
        print("{:<15} {:<10} {:<10} {:<10}".format("Bill Month", "Group 1", "Group 2", "Total"))
        for row in report_data:
            print("{:<15} {:<10} {:<10} {:<10}".format(row[0], row[1], row[2], row[3]))

        return report_data

    except cx_Oracle.DatabaseError as e:
        print("Database error:", e)
        return None

    finally:
        if connection:
            connection.close()

def get_group_transactions(group_id):
    """
    Get the list of transactions for a specific group by group_id.
    Returns a list of transactions with their details.
    """
    connection = None
    try:
        # Establish the database connection
        connection = get_connection()
        cursor = connection.cursor()

        # Query to get the transactions for the given group_id
        query = """
            SELECT transactionid, amount, "date", description, payerid, payeeid, status, billid
            FROM "IS150403".transaction
            WHERE groupid = :group_id
            ORDER BY "date" DESC
        """

        # Execute the query using parameterized input
        cursor.execute(query, {"group_id": group_id})

        # Fetch all results
        transactions = cursor.fetchall()

        # Return the list of transactions (each item is a tuple)
        return transactions

    except cx_Oracle.DatabaseError as e:
        # Log or handle the database error
        print("Database error:", e)
        return []

    finally:
        # Close the connection if it was established
        if connection:
            connection.close()
