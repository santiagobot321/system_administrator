import os
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from typing import List

# --- Lógica del Servidor FastAPI y WebSocket (Todo en un solo archivo) ---

# 1. Gestor de Conexiones WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

# 2. Creación de la App FastAPI
# Gunicorn buscará esta variable 'app' por defecto si se lo indicamos.
app = FastAPI()

# 3. Configuración de Rutas de Archivos Estáticos
# Apuntamos a la carpeta `frontend` que está en la raíz del proyecto.
# Usamos una ruta relativa simple, ya que Render ejecuta desde la raíz.
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# 4. Endpoint WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# 5. API para que React obtenga la lista de equipos
@app.get("/api/equipos", response_class=JSONResponse)
def get_equipos_api():
    # Devolvemos datos falsos para la demo, para no depender de otros servicios.
    return [
        {"id": 1, "hostname": "PC-SALA-01", "ip": "192.168.1.50"},
        {"id": 2, "hostname": "PC-SALA-02", "ip": "192.168.1.51"},
        {"id": 3, "hostname": "SERVIDOR-PROY", "ip": "192.168.1.52"},
    ]

# 6. API para que React dispare el ataque
@app.get("/actions/simulate-attack/{ip}")
async def simulate_attack(ip: str):
    await manager.broadcast({"type": "attack", "ip": ip})
    return {"status": "attack signal sent"}

# --- Punto de entrada para Uvicorn (si se ejecuta localmente) ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
