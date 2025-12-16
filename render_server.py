import os
import sys

# --- SOLUCIÓN AL ModuleNotFoundError (La forma correcta) ---
# Añadimos la ruta raíz del proyecto al sys.path para que Python encuentre el módulo 'backend'.
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# -------------------------------------------------------------

# --- Importamos la aplicación REAL desde su ubicación correcta ---
from backend.main import app

# --- Punto de entrada para Uvicorn (si se ejecuta localmente) ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    # Ejecutamos la 'app' que importamos de backend.main
    uvicorn.run(app, host="0.0.0.0", port=port)
