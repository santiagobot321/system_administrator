import os
import uvicorn
# Importamos la aplicación FastAPI desde nuestro módulo de simulación
from agent.simulation_server.server import app as simulation_app

if __name__ == "__main__":
    # Render proporciona la variable de entorno PORT para decirnos en qué puerto escuchar.
    # Usamos 8000 como valor por defecto si corremos localmente.
    port = int(os.environ.get("PORT", 8000))
    
    # Al desplegar, Gunicorn manejará esto, pero es bueno tenerlo para pruebas locales.
    uvicorn.run(simulation_app, host="0.0.0.0", port=port)
