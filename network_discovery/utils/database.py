import mysql.connector
from mysql.connector import Error

def get_host_name_by_address(host_address):
    try:
        connection = mysql.connector.connect(
            host="10.230.230.200", database="centreon", user="root", password="snms"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT host_name FROM host WHERE host_address = %s"
            cursor.execute(query, (host_address,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return host_address
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()