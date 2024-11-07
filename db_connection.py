import cx_Oracle

# Database connection settings
HOST = "your_host"
PORT = "your_port"
SERVICE_NAME = "your_service_name"
USER = "IS150403"
PASSWORD = "your_password"

def get_connection():
    """
    Establish and return a database connection using cx_Oracle.
    """
    dsn = cx_Oracle.makedsn(HOST, PORT, service_name=SERVICE_NAME)
    connection = cx_Oracle.connect(user=USER, password=PASSWORD, dsn=dsn)
    return connection

def check_user_exists(username, email, phone):
    """
    Check if a user exists in the database.
    Returns True if the user exists, otherwise False.
    """
    connection = None
    try:
        # Establish the database connection
        connection = get_connection()
        cursor = connection.cursor()

        # Query to check if the user exists
        query = """
            SELECT * FROM "User"
            WHERE NAME = :username AND EMAIL = :email AND PHONE = :phone
        """
        cursor.execute(query, {"username": username, "email": email, "phone": phone})
        result = cursor.fetchone()

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
