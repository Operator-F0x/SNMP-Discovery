import sqlite3
import os

class DatabaseManager:
    def __init__(self):
        # Path to the SQLite database file
        self.db_path = os.getenv('DB_PATH', 'database.db')

    def get_host_name_by_address(self, host_address):
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            print("Connected to SQLite database.")

            # Query to retrieve the host name
            query = "SELECT host_name FROM host WHERE host_address = ?"
            cursor.execute(query, (host_address,))
            result = cursor.fetchone()

            # Return the host name or the host address if not found
            return result[0] if result else host_address
        except sqlite3.Error as e:
            print(f"Error while connecting to SQLite: {e}")
            return None
        finally:
            # Close the connection
            if connection:
                connection.close()
                print("SQLite connection closed.")

# Example usage:
# Make sure to set the DB_PATH environment variable or the default database will be 'database.db'
