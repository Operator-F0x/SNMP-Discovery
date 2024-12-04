import mysql.connector
from mysql.connector import Error
import os
from utils.network import save_local_ip_to_env

def get_host_name_by_address(host_address):
    """
    Retrieve the host name associated with a given host address from the Centreon database.

    This function connects to a MySQL database, executes a query to find the host name
    corresponding to the provided host address, and returns the host name if found.
    If the host address is not found in the database, the function returns the host address itself.

    Parameters:
    host_address (str): The IP address of the host to look up.

    Returns:
    str: The host name associated with the given host address, or the host address if not found.
    None: If there is an error while connecting to the database.

    Example:
    >>> get_host_name_by_address("192.168.1.1")
    'example-hostname'

    >>> get_host_name_by_address("10.0.0.1")
    '10.0.0.1'  # If the host address is not found in the database

    Note:
    Ensure that the MySQL server is running and accessible, and that the provided
    connection details (host, database, user, password) are correct.

    Raises:
    mysql.connector.Error: If there is an error while connecting to the MySQL database.
    """
    try:
        db_host = os.getenv('DB_HOST')
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')

        # Establish the database connection
        connection = mysql.connector.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        
        if connection.is_connected():
            print("Connected to MySQL database.")
            cursor = connection.cursor()
            query = "SELECT host_name FROM host WHERE host_address = %s"
            cursor.execute(query, (host_address,))
            result = cursor.fetchone()
            return result[0] if result else host_address
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")
