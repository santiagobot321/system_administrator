import os
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List

# --- Lógica del Servidor Completo (API + WebSockets + HTML) ---

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
app = FastAPI()

# 3. Configuración de Plantillas y Archivos Estáticos
# Apuntamos a la carpeta `frontend` que está en la raíz del proyecto.
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# --- Endpoints que Sirven las Páginas HTML ---

@app.get("/", response_class=HTMLResponse)
def get_attacker_console(request: Request):
    """ Sirve el panel del atacante como página principal para la demo. """
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/attendee", response_class=HTMLResponse)
async def get_attendee_page(request: Request):
    """ Sirve la página para los móviles de los asistentes. """
    return templates.TemplateResponse("attendee.html", {"request": request})

@app.get("/attack", response_class=HTMLResponse)
def get_attacker_console(request: Request):
    """ Sirve el panel del atacante como página principal para la demo. """
    return templates.TemplateResponse("attacker.html", {"request": request})

# --- Endpoints de la API y WebSockets ---

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/equipos", response_class=JSONResponse)
def get_equipos_api():
    """
    Devuelve datos de equipos. Para la demo en Render, usamos datos quemados
    para no depender de una base de datos externa, haciendo la demo más robusta.
    """
    return [
        {"id": 1, "hostname": "PC-SALA-01", "ip": "192.168.1.50"},
        {"id": 2, "hostname": "PC-SALA-02", "ip": "192.168.1.51"},
        {"id": 3, "hostname": "SERVIDOR-PROY", "ip": "192.168.1.52"},
    ]

@app.get("/actions/simulate-attack/{ip}")
async def simulate_attack(ip: str):
    """ Dispara la alerta a todos los clientes conectados. """
    await manager.broadcast({"type": "attack", "ip": ip})
    return {"status": "attack signal sent"}

# --- Punto de entrada para Uvicorn/Gunicorn ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
