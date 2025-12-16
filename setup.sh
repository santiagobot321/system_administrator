#!/bin/bash

# Salir si hay errores
set -e

echo "🔧 Instalando dependencias del sistema (Arch)..."
sudo pacman -Syu --noconfirm \
    python \
    python-pip \
    python-virtualenv \
    mariadb \
    mariadb-clients \
    gcc \
    base-devel

echo "📦 Creando y activando entorno virtual..."
python -m venv venv
source venv/bin/activate

echo "🐍 Instalando dependencias de Python..."
pip install --upgrade pip
pip install \
    fastapi \
    uvicorn[standard] \
    jinja2 \
    python-multipart \
    passlib[bcrypt] \
    itsdangerous \
    mariadb \
    sqlalchemy

echo "⚙️ Configurando MariaDB..."

# Inicializar data directory solo si no existe
if [ ! -d "/var/lib/mysql/mysql" ]; then
    sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
fi

sudo systemctl enable mariadb
sudo systemctl start mariadb

echo "📂 Creando base de datos y tablas..."
sudo mariadb <<EOF
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
python tools/create_admin.py

echo "🚀 Iniciando servidor de desarrollo..."
uvicorn backend.main:app --host 0.0.0.0 --reload
