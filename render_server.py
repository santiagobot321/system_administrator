import os
import sys
import uvicorn

# --- SOLUCIÓN AL ModuleNotFoundError ---
# 1. Obtenemos la ruta absoluta del directorio donde se encuentra este archivo (la raíz del proyecto en Render).
#    En Render, esto será /opt/render/project/src
project_root = os.path.dirname(os.path.abspath(__file__))

# 2. Añadimos esta ruta al sys.path de Python.
#    Esto le dice a Python que busque módulos aquí.
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# -----------------------------------------

# Ahora, esta importación debería funcionar sin problemas.
from agent.simulation_server.server import app as simulation_app

if __name__ == "__main__":
    # Render proporciona la variable de entorno PORT para decirnos en qué puerto escuchar.
    # Usamos 8000 como valor por defecto si corremos localmente.
    port = int(os.environ.get("PORT", 8000))
    
    # Al desplegar, Gunicorn manejará esto, pero es bueno tenerlo para pruebas locales.
    uvicorn.run(simulation_app, host="0.0.0.0", port=port)
