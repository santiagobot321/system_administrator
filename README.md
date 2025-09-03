# 🖥️ Riwimanager

**Riwimanager** es un prototipo funcional para la **administración remota de equipos** en una red local. Permite encender, apagar y mostrar contenido en pantalla de los equipos cliente desde una interfaz centralizada.

---

## 📌 Descripción

Este proyecto nace para resolver un problema común en redes con múltiples PCs: tener que configurar y administrar cada una manualmente. **Riwimanager** busca simplificar estas tareas permitiendo:

- Encender/apagar equipos remotamente
- Mostrar contenido (por ejemplo, videos) en las pantallas de los clientes
- Gestionar el estado de cada equipo
- Login seguro del administrador de sistemas

🧪 Es un proyecto en desarrollo, con vistas a incorporar en el futuro:
- Configuración remota de sistemas operativos (incluyendo dual boot)
- Instalación automática de programas
- Actualizaciones y mantenimiento de software vía red

---

## ⚙️ Tecnologías usadas

- **Backend:** Python 3.12, FastAPI
- **Base de datos:** MariaDB
- **Frontend:** HTML + Jinja2 + CSS
- **ORM:** SQLAlchemy
- **Autenticación:** Passlib (bcrypt), Itsdangerous
- **Otros:** Wake-on-LAN, sistema de plantillas, manejo de formularios

---

## 🧩 Estructura del proyecto

riwimanager/
├── backend/
│ ├── routes/ # Rutas de FastAPI
│ ├── templates/ # HTML + CSS
│ ├── static/ # Archivos estáticos (CSS, imágenes)
│ ├── main.py # Punto de entrada de la app
│ ├── db.py # Conexión a la base de datos
│ ├── auth.py # Lógica de login
│ └── session.py # Gestión de sesiones
├── tools/ # Scripts utilitarios
│ ├── create_admin.py # Crear primer usuario admin
│ ├── wol.py # Wake-on-LAN
│ └── update_system.py # Placeholder para actualizaciones
├── setup.sh # Script de instalación y despliegue local
├── README.md
└── .gitignore


---

## 🚀 Instalación y ejecución local

### Requisitos previos

- Ubuntu/Debian
- Python 3.12
- Git

### 🔧 Paso a paso


# Clonar el repositorio
- git clone https://github.com/santiagobot321/system_administrator.git
- cd
- riwimanager

# Dar permisos al instalador
chmod +x setup.sh

# Ejecutar el script de instalación y despliegue local
./setup.sh


<img width="1920" height="958" alt="image" src="https://github.com/user-attachments/assets/1c485bb5-0fc2-4002-8b7f-c647044fa6f4" />

<img width="1920" height="958" alt="image" src="https://github.com/user-attachments/assets/24b8fc39-5a1d-4158-8514-a81112df54e4" />


