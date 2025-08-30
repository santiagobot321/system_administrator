import sys
import os
import mariadb

# --- Configuración de la ruta para importar desde 'backend' ---
# Esto permite que el script se ejecute desde el directorio raíz del proyecto
# (ej: python3 scripts/create_admin.py) y encuentre los módulos necesarios.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
# -------------------------------------------------------------

from backend.database import get_db_connection
from backend.auth import get_password_hash

# --- Detalles del usuario administrador ---
ADMIN_EMAIL = "admin@riwi.com"
ADMIN_PASSWORD = "1234"

def setup_admin_user():
    """
    Se conecta a la base de datos, crea la tabla 'users' si no existe,
    y añade el usuario administrador si no ha sido creado previamente.
    """
    conn = None
    try:
        print("Conectando a la base de datos...")
        conn = get_db_connection()
        cur = conn.cursor()

        print("Asegurando que la tabla 'users' exista...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL
            )
        """)

        print(f"Asegurando que el usuario administrador '{ADMIN_EMAIL}' exista y esté actualizado...")
        hashed_password = get_password_hash(ADMIN_PASSWORD)
        print(f"  -> Hash generado: {hashed_password}")

        # Usamos INSERT ... ON DUPLICATE KEY UPDATE para crear o actualizar al admin.
        # Esto es más eficiente que hacer un SELECT primero.
        cur.execute("""
            INSERT INTO users (email, password_hash)
            VALUES (?, ?)
            ON DUPLICATE KEY UPDATE password_hash = VALUES(password_hash)
        """, (ADMIN_EMAIL, hashed_password))
        conn.commit()

        if cur.rowcount == 1:
            print("\n¡Usuario administrador creado exitosamente!")
        elif cur.rowcount == 2: # En MariaDB, una actualización cuenta como 2 filas afectadas
            print(f"\nLa contraseña del usuario administrador '{ADMIN_EMAIL}' ha sido actualizada.")
        else:
            print(f"\nEl usuario administrador '{ADMIN_EMAIL}' ya existía con la contraseña correcta.")
        print(f"  -> Email: {ADMIN_EMAIL}")
        print(f"  -> Contraseña: {ADMIN_PASSWORD}")

    except mariadb.Error as e:
        print(f"Error de base de datos: {e}")
    finally:
        if conn:
            conn.close()
            print("\nConexión a la base de datos cerrada.")

if __name__ == "__main__":
    setup_admin_user()