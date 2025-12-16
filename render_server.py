import os
import sys
import uvicorn

# --- SOLUCIÓN AL ModuleNotFoundError ---
# Añadimos la ruta raíz al sys.path para asegurar que Python encuentre los módulos.
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# -----------------------------------------

# --- IMPORTACIÓN CORREGIDA ---
# Ahora usamos 'agents' (plural) para que coincida con el nombre de tu carpeta.
from agents.simulation_server.server import app as simulation_app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(simulation_app, host="0.0.0.0", port=port)
