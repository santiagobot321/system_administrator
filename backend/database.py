import mariadb
import sys

#  Cargar esto desde variables de entorno en lugar de hardcodearlo.
# Asegúrate de que la contraseña sea la correcta para tu usuario root de MariaDB.
DB_CONFIG = {
    'user': 'root',
    'password': '',  
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'administrator_system'
}

def get_db_connection():
    try:
        conn = mariadb.connect(**DB_CONFIG)
        return conn
    except mariadb.Error as e:
        print(f"Error conectando a la base de datos MariaDB: {e}")
        sys.exit(1)