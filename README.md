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
├── agents/                          # Agentes (clientes) para monitorear equipos (por desarrollar)
├── backend/                         # Backend principal con FastAPI
│   ├── routes/                      # Rutas de la API
│   │   ├── utils/                   # Utilidades varias
│   │   ├── auth.py                  # Rutas de autenticación
│   │   └── equipos.py               # Rutas para gestión de equipos
│   ├── templates/                   # Archivos HTML (Jinja2) y recursos estáticos
│   │   ├── static/
│   │   │   ├── imag/                # Carpeta para imágenes
│   │   │   └── style.css            # Estilos del frontend
│   │   ├── base.html                # Plantilla base
│   │   ├── login.html               # Formulario de inicio de sesión
│   │   └── reportes.html            # Página de reportes (en desarrollo)
│   ├── auth.py                      # Lógica de autenticación
│   ├── database.py                  # Conexión a la base de datos (MariaDB)
│   ├── db.py                        # Archivo auxiliar o legado (no utilizado)
│   ├── main.py                      # Punto de entrada de la app FastAPI
│   └── session.py                   # Gestión de sesión de usuario
├── infrastructure/                 # Infraestructura del sistema (por desarrollar)
├── tools/                          # Herramientas para administración remota
│   ├── create_admin.py             # Script para crear un usuario administrador
│   ├── host.py                     # Script para apagar equipos de forma remota
│   ├── install.py                  # Instalación remota de software (ej: VSCode)
│   ├── update_system.py            # Script de actualización del sistema
│   └── wol.py                      # Envío de paquetes Wake-On-LAN
├── venv/                           # Entorno virtual de Python (no incluir en Git)
├── .gitignore                      # Archivos y carpetas ignoradas por Git
├── README.md                       # Documentación del proyecto
└── setup.sh                        # Script de instalación y despliegue local



---

## 🚀 Instalación y ejecución local

### Requisitos previos

- Ubuntu/Debian
- Python 3.12
- Git

# 🔧 Paso a paso


## Clonar el repositorio
- git clone https://github.com/santiagobot321/system_administrator.git
- cd
- riwimanager

## Dar permisos al instalador
chmod +x setup.sh

## Ejecutar el script de instalación y despliegue local
./setup.sh

<img width="1920" height="958" alt="image" src="https://github.com/user-attachments/assets/24b8fc39-5a1d-4158-8514-a81112df54e4" />

<img width="1920" height="958" alt="image" src="https://github.com/user-attachments/assets/50212791-4a2e-4fb1-a30a-e73ee91fda63" />





