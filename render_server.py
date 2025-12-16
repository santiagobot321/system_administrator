import os
from fastapi import FastAPI, Request, Form, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from typing import List, Dict, Any

# --- 1. "Base de Datos" en Memoria ---
# Única fuente de verdad para toda la aplicación.
EQUIPOS_DB: List[Dict[str, Any]] = [
    {"id": 1, "hostname": "PC-SALA-01", "ip": "192.168.1.50", "mac": "00:1A:2B:3C:4D:5E", "estado": "En línea", "conectado": True, "error": None},
    {"id": 2, "hostname": "PC-SALA-02", "ip": "192.168.1.51", "mac": "00:1A:2B:3C:4D:5F", "estado": "Desconocido", "conectado": False, "error": None},
    {"id": 3, "hostname": "SERVIDOR-PROY", "ip": "192.168.1.52", "mac": "00:1A:2B:3C:4D:60", "estado": "Error de red", "conectado": False, "error": "No responde al ping"},
]

# --- 2. Lógica del Servidor Completo ---

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
app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# --- 3. Endpoints que Sirven las Páginas HTML ---

@app.get("/", response_class=HTMLResponse)
def get_dashboard(request: Request):
    """ Sirve el dashboard principal (`base.html`) con la lista de equipos de nuestra DB en memoria. """
    return templates.TemplateResponse("base.html", {"request": request, "equipos": EQUIPOS_DB})

@app.get("/attendee", response_class=HTMLResponse)
async def get_attendee_page(request: Request):
    return templates.TemplateResponse("attendee.html", {"request": request})

@app.get("/attack", response_class=HTMLResponse)
def get_attacker_console(request: Request):
    return templates.TemplateResponse("attacker.html", {"request": request})

# --- 4. Endpoints de Acciones (El motor que faltaba) ---

@app.post("/equipos/add", response_class=RedirectResponse)
async def agregar_equipo(hostname: str = Form(...), mac: str = Form(...), ip: str = Form(...)):
    new_id = max(e["id"] for e in EQUIPOS_DB) + 1 if EQUIPOS_DB else 1
    EQUIPOS_DB.append({
        "id": new_id, "hostname": hostname, "mac": mac, "ip": ip,
        "estado": "Añadido", "conectado": False, "error": None
    })
    return RedirectResponse(url="/", status_code=303)

@app.get("/equipos/delete/{equipo_id}", response_class=RedirectResponse)
async def eliminar_equipo(equipo_id: int):
    global EQUIPOS_DB
    EQUIPOS_DB = [e for e in EQUIPOS_DB if e["id"] != equipo_id]
    return RedirectResponse(url="/", status_code=303)

# Rutas para los botones de acción. No hacen nada "real" en Render,
# pero evitan el 404 y redirigen, haciendo que la UI se sienta funcional.
@app.get("/actions/{action}/{param}", response_class=RedirectResponse)
async def handle_action(action: str, param: str):
    print(f"ACCIÓN SIMULADA: {action} en {param}")
    # Simplemente redirigimos al dashboard para que el usuario vea que "algo pasó".
    return RedirectResponse(url="/", status_code=303)

# --- 5. Endpoints de la API y WebSockets ---

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
    """ La API del atacante ahora lee de la misma DB en memoria, asegurando sincronización. """
    return EQUIPOS_DB

@app.get("/actions/simulate-attack/{ip}")
async def simulate_attack(ip: str):
    await manager.broadcast({"type": "attack", "ip": ip})
    return {"status": "attack signal sent"}

# --- Punto de entrada para Uvicorn/Gunicorn ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
