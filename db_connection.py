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
        WITH user_total_paid AS (
            SELECT t.payerid AS userid,
                   b.groupid,
                   SUM(t.amount) AS total_paid
            FROM transaction t
            JOIN bill b ON t.billid = b.billid
            WHERE t.status = 'approved' AND b.groupid = :group_id
            GROUP BY t.payerid, b.groupid
        )
        SELECT u.name,
               get_user_total_debt(u.userid) AS total_debt,
               NVL(utp.total_paid, 0) AS total_paid,
               CASE 
                   WHEN NVL(utp.total_paid, 0) >= get_user_total_debt(u.userid) THEN 'Paid'
                   ELSE 'Indebted'
               END AS payment_status,
               ROUND((NVL(utp.total_paid, 0) / get_user_total_debt(u.userid)) * 100, 2) AS percentage_paid
        FROM "User" u
        JOIN user_group ug ON u.userid = ug.userid
        LEFT JOIN user_total_paid utp ON u.userid = utp.userid AND ug.groupid = utp.groupid
        WHERE ug.groupid = :group_id
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
