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
