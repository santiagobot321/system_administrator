from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Any
import os

# --- Importamos la lógica de sesión para proteger las rutas ---
from backend.session import get_user_or_redirect

# --- 1. "Base de Datos" en Memoria ---
EQUIPOS_DB: List[Dict[str, Any]] = [
    {"id": 1, "hostname": "PC-SALA-01", "ip": "192.168.1.50", "mac": "00:1A:2B:3C:4D:5E", "estado": "En línea", "conectado": True, "error": None},
    {"id": 2, "hostname": "PC-SALA-02", "ip": "192.168.1.51", "mac": "00:1A:2B:3C:4D:5F", "estado": "Desconocido", "conectado": False, "error": None},
    {"id": 3, "hostname": "SERVIDOR-PROY", "ip": "192.168.1.52", "mac": "00:1A:2B:3C:4D:60", "estado": "Error de red", "conectado": False, "error": "No responde al ping"},
]

router = APIRouter()

# Apuntamos a la carpeta `frontend` que está en la raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATES_DIR = os.path.join(BASE_DIR, "frontend/templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# --- Rutas que usan la DB en memoria ---

@router.get("/", response_class=HTMLResponse)
def listar_equipos_page(request: Request, user: str = Depends(get_user_or_redirect)):
    """ Sirve el dashboard principal con la lista de equipos de nuestra DB en memoria. """
    return templates.TemplateResponse("base.html", {"request": request, "equipos": EQUIPOS_DB})

@router.get("/api/equipos", response_class=JSONResponse)
def listar_equipos_api(user: str = Depends(get_user_or_redirect)):
    """ La API del atacante ahora lee de la misma DB en memoria. """
    return EQUIPOS_DB

@router.post("/add", response_class=RedirectResponse)
async def agregar_equipo(hostname: str = Form(...), mac: str = Form(...), ip: str = Form(...), user: str = Depends(get_user_or_redirect)):
    new_id = max(e["id"] for e in EQUIPOS_DB) + 1 if EQUIPOS_DB else 1
    EQUIPOS_DB.append({
        "id": new_id, "hostname": hostname, "mac": mac, "ip": ip,
        "estado": "Añadido", "conectado": False, "error": None
    })
    return RedirectResponse(url="/equipos/", status_code=303)

@router.get("/delete/{equipo_id}", response_class=RedirectResponse)
async def eliminar_equipo(equipo_id: int, user: str = Depends(get_user_or_redirect)):
    global EQUIPOS_DB
    EQUIPOS_DB = [e for e in EQUIPOS_DB if e["id"] != equipo_id]
    return RedirectResponse(url="/equipos/", status_code=303)
