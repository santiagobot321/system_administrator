#!/bin/bash

# Salir si hay errores
set -e

echo "🔧 Instalando dependencias del sistema..."
sudo apt update
sudo apt install -y python3.12-venv python3.12-dev libmariadb-dev mariadb-server mariadb-client

echo "📦 Creando y activando entorno virtual..."
python3.12 -m venv venv
source venv/bin/activate

echo "🐍 Instalando dependencias de Python..."
pip install --upgrade pip
pip install fastapi uvicorn[standard] jinja2 python-multipart passlib[bcrypt] itsdangerous mariadb sqlalchemy

echo "✅ Dependencias instaladas."

echo "⚙️ Configurando MariaDB..."
sudo systemctl start mariadb
sudo systemctl enable mariadb

echo "📂 Creando base de datos y tablas..."
sudo mariadb -u root <<EOF
CREATE DATABASE IF NOT EXISTS administrator_system;
USE administrator_system;

CREATE TABLE IF NOT EXISTS equipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hostname VARCHAR(100) NOT NULL,
    mac VARCHAR(17) NOT NULL UNIQUE,
    ip VARCHAR(15) NOT NULL UNIQUE,
    estado VARCHAR(50),
    conectado BOOLEAN DEFAULT FALSE,
    error TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);
EOF

echo "👤 Creando usuario administrador..."
python3 tools/create_admin.py

echo "🚀 Iniciando servidor de desarrollo..."
uvicorn backend.main:app --reload
