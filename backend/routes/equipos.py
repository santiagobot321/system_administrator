from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from backend.database import get_db_connection
import subprocess
from backend.session import get_user_or_redirect
from tools.wol import send_wol


router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

class EstadoEquipo(BaseModel):
    hostname: str
    ip: str
    red: bool
    internet: bool

@router.post("/report")
def recibir_estado(estado: EstadoEquipo):
    conn = get_db_connection()
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
    conn = get_db_connection()
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
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, hostname, mac, ip, estado, conectado, error FROM equipos")
    equipos = cur.fetchall()
    conn.close()
    return templates.TemplateResponse("base.html", {"request": request, "equipos": equipos})

# --- Agregar equipo ---
@router.post("/add", response_class=RedirectResponse)
async def agregar_equipo(
    hostname: str = Form(...),
    mac: str = Form(...),
    ip: str = Form(...),
    estado: str = Form("desconocido"),
    user: str = Depends(get_user_or_redirect)
):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO equipos (hostname, mac, ip, estado) VALUES (?, ?, ?, ?)", (hostname, mac, ip, estado))
        conn.commit()
    finally:
        if conn:
            conn.close()
    return RedirectResponse(url="/", status_code=303)

# --- Eliminar equipo ---
@router.get("/delete/{id}", response_class=RedirectResponse)
async def eliminar_equipo(id: int, user: str = Depends(get_user_or_redirect)):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM equipos WHERE id=?", (id,))
        conn.commit()
    finally:
        if conn:
            conn.close()
    return RedirectResponse(url="/", status_code=303)

# --- Encender equipo (WOL) ---
@router.get("/encender/{mac}", response_class=RedirectResponse)
async def encender_equipo(mac: str, user: str = Depends(get_user_or_redirect)):
    try:
        print(f"Enviando Magic Packet a la MAC: {mac}")
        send_wol(mac)
    except Exception as e:
        print(f"Error al intentar encender el equipo {mac}: {e}")
        # En una aplicación más avanzada, aquí se podría mostrar un mensaje de error al usuario.
    return RedirectResponse(url="/", status_code=303)

# --- Apagar equipo ---
@router.get("/apagar/{ip}")
def apagar_equipo(ip: str):
    subprocess.run(["python3", "tools/host.py", ip])
    return RedirectResponse("/", status_code=303)

# --- Instalar VSCode ---
@router.get("/instalar/{ip}")
def instalar_vscode_equipo(ip: str):
    subprocess.run(["python3", "tools/install.py", ip])
    return RedirectResponse("/", status_code=303)

# --- Mostrar bienvenida ---
@router.get("/bienvenida/{ip}")
def mostrar_bienvenida(ip: str):
    subprocess.run(["python3", "tools/install.py", ip])
    return RedirectResponse("/", status_code=303)

