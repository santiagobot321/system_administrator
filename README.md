# system_administrator
Para que tu app funcione bien, necesitas instalar:
# Crear y activar entorno virtual
sudo apt install python3.12-venv -y

python3 -m venv venv

source venv/bin/activate

# Instalar dependencias de Python
pip install fastapi uvicorn[standard] jinja2 python-multipart passlib[bcrypt] itsdangerous

sudo apt install libmariadb-dev

sudo apt install python3.12-dev

pip install mariadb sqlalchemy

👉 Explicación:

fastapi → framework principal.

uvicorn[standard] → servidor ASGI para correr FastAPI.
passlib[bcrypt] → para hashear y verificar contraseñas de forma segura.

jinja2 → renderizar templates HTML.

python-multipart → si vas a manejar formularios o subir archivos.

mariadb → conector oficial para MariaDB.

sqlalchemy → ORM recomendado para manejar base de datos (más fácil que escribir SQL directo).


Configuración de MariaDB

Instalar MariaDB (si no lo hiciste):


sudo apt install mariadb-server mariadb-client -y

sudo systemctl start mariadb

sudo systemctl enable mariadb


sudo mariadb -u root


-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS administrator_system;

-- Seleccionar la base de datos
USE administrator_system;

-- Crear la tabla
CREATE TABLE IF NOT EXISTS equipos (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    hostname VARCHAR(255) NOT NULL,     
    mac VARCHAR(17) NOT NULL,           
    ip VARCHAR(15) NOT NULL,            
    estado VARCHAR(50) NOT NULL         
);

-- Crear la tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);


Crear el primer usuario administrador

python3 scripts/create_admin.py



uvicorn backend.main:app --reload
