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
