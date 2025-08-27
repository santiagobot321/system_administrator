from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from backend.db import get_connection
import subprocess

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

class EstadoEquipo(BaseModel):
    hostname: str
    ip: str
    red: bool
    internet: bool

@router.post("/report")
def recibir_estado(estado: EstadoEquipo):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE equipos SET estado=%s, conectado=%s WHERE hostname=%s
    """, (
        f"Red: {estado.red}, Internet: {estado.internet}",
        estado.red and estado.internet,
        estado.hostname
    ))
    conn.commit()
    conn.close()
    return {"msg": "Estado recibido"}

class ErrorReport(BaseModel):
    hostname: str
    error: str

@router.post("/error")
def recibir_error(error: ErrorReport):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE equipos SET error=%s WHERE hostname=%s
    """, (error.error, error.hostname))
    conn.commit()
    conn.close()
    return {"msg": "Error recibido"}



# --- Listar equipos ---
@router.get("/")
def listar_equipos(request: Request):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, hostname, mac, ip, estado FROM equipos")
    equipos = cur.fetchall()
    conn.close()
    return templates.TemplateResponse("base.html", {"request": request, "equipos": equipos})

# --- Agregar equipo ---
@router.post("/add")
def agregar_equipo(hostname: str = Form(...), mac: str = Form(...), ip: str = Form(...), estado: str = Form("desconocido")):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO equipos (hostname, mac, ip, estado) VALUES (%s, %s, %s, %s)", (hostname, mac, ip, estado))
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=303)

# --- Eliminar equipo ---
@router.get("/delete/{id}")
def eliminar_equipo(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM equipos WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=303)

# --- Encender equipo (WOL) ---
@router.get("/encender/{mac}")
def encender_equipo(mac: str):
    subprocess.run(["python3", "tools/wol.py", mac])
    return RedirectResponse("/", status_code=303)

# --- Apagar equipo ---
@router.get("/apagar/{ip}")
def apagar_equipo(ip: str):
    subprocess.run(["python3", "tools/host.py", ip])
    return RedirectResponse("/", status_code=303)
