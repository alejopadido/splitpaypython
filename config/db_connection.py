import os
import cx_Oracle

# Add Oracle Instant Client path to environment variable
os.environ["PATH"] = r"C:\Users\alejo\dev\instantclient_23_6;" + os.environ["PATH"]


# Database connection settings
HOST = "orion.javeriana.edu.co"
PORT = "1521"
SERVICE_NAME = "LAB"
USER = "is150403"
PASSWORD = "eTvw97#g#qyrift"

def get_connection():
    """
    Establish and return a database connection using cx_Oracle.
    """
    dsn = cx_Oracle.makedsn(HOST, PORT, service_name=SERVICE_NAME)
    connection = cx_Oracle.connect(user=USER, password=PASSWORD, dsn=dsn)
    if connection != None: print('Connection successful!')
    return connection

def check_user_exists(username, email, phone):
    print('Username: ' + username + " Email: " + email + " Phone: " + phone)
    """
    Check if a user exists in the database.
    Returns True if the user exists, otherwise False.
    """
    connection = None
    try:
        # Establish the database connection
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM "IS150403"."User"')
        tables = cursor.fetchall()
        print("Existing Users:", tables)

        # Query to check if the user exists
        query = """
            SELECT * FROM "IS150403"."User"
        """
        # cursor.execute(query, {"username": username, "email": email, "phone": phone})
        cursor.execute(query)
        
        result = cursor.fetchone()
        print('Login result: ', result)
        # If a result is found, the user exists
        return result is not None

    except cx_Oracle.DatabaseError as e:
        # Log or handle the database error
        print("Database error:", e)
        return False

    finally:
        # Close the connection if it was established
        if connection:
            connection.close()
