import mariadb
import sys

# It's highly recommended to load these values from environment variables or a config file
# instead of hardcoding them, especially for production environments.
# Make sure the password is correct for your MariaDB user.
DB_CONFIG = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'administrator_system1'
}

def get_db_connection():
    try:
        # Establish a connection to the database using the configuration dictionary.
        # The ** operator unpacks the dictionary into keyword arguments.
        conn = mariadb.connect(**DB_CONFIG)
        return conn
    except mariadb.Error as e:
        # If a connection error occurs, print a detailed error message to the console.
        print(f"Error connecting to MariaDB Database: {e}")
        # Exit the script with a non-zero status code to indicate that a fatal
        # error has occurred. This is crucial for scripts that depend on the database.
        sys.exit(1)