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

# Pydantic model for validating the payload from an agent's status report.
class EstadoEquipo(BaseModel):
    hostname: str
    ip: str
    red: bool
    internet: bool

@router.post("/report")
def recibir_estado(estado: EstadoEquipo):
    """
    Receives a status report from a client agent.
    Updates the computer's status, connectivity, and network details in the database.
    """
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

# Pydantic model for validating the payload from an agent's error report.
class ErrorReport(BaseModel):
    hostname: str
    error: str

@router.post("/error")
def recibir_error(error: ErrorReport):
    """
    Receives an error report from a client agent.
    Updates the computer's error field in the database.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE equipos SET error=%s WHERE hostname=%s
    """, (error.error, error.hostname))
    conn.commit()
    conn.close()
    return {"msg": "Error recibido"}



# --- List Computers ---
@router.get("/")
def listar_equipos(request: Request, user: str = Depends(get_user_or_redirect)):
    """
    Displays the main dashboard page, listing all computers from the database.
    This route is protected and requires the user to be logged in.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, hostname, mac, ip, estado, conectado, error FROM equipos")
    equipos = cur.fetchall()
    conn.close()
    return templates.TemplateResponse("base.html", {"request": request, "equipos": equipos})

# --- Add Computer ---
@router.post("/add", response_class=RedirectResponse)
async def agregar_equipo(
    hostname: str = Form(...),
    mac: str = Form(...),
    ip: str = Form(...),
    estado: str = Form("desconocido"),
    # This dependency ensures that only authenticated users can add a computer.
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

# --- Delete Computer ---
@router.get("/delete/{id}", response_class=RedirectResponse)
async def eliminar_equipo(id: int, user: str = Depends(get_user_or_redirect)):
    """
    Deletes a computer from the database based on its ID.
    Protected route.
    """
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

# --- Turn On Computer (WOL) ---
@router.get("/encender/{mac}", response_class=RedirectResponse)
async def encender_equipo(mac: str, user: str = Depends(get_user_or_redirect)):
    """
    Sends a Wake-on-LAN (WOL) magic packet to the specified MAC address.
    Protected route.
    """
    try:
        print(f"Sending Magic Packet to MAC: {mac}")
        send_wol(mac)
    except Exception as e:
        print(f"Error trying to turn on computer {mac}: {e}")
        # In a more advanced application, an error message could be displayed to the user here.
    return RedirectResponse(url="/", status_code=303)

# --- Turn Off Computer ---
@router.get("/apagar/{ip}")
def apagar_equipo(ip: str, user: str = Depends(get_user_or_redirect)):
    """
    Sends a shutdown command to the agent on the specified IP.
    This is done by executing an external Python script.
    Protected route.
    """
    # Note: The 'host.py' script is not provided, but it's assumed to handle the client-side command.
    subprocess.run(["python3", "tools/host.py", ip])
    return RedirectResponse("/", status_code=303)

# --- Install VSCode (Example) ---
@router.get("/instalar/{ip}")
def instalar_vscode_equipo(ip: str, user: str = Depends(get_user_or_redirect)):
    """
    Sends a command to the agent to install an application (e.g., VSCode).
    This is a placeholder and currently calls the same script as 'mostrar_bienvenida'.
    Protected route.
    """
    subprocess.run(["python3", "tools/install.py", ip])
    return RedirectResponse("/", status_code=303)

# --- Show Welcome Message ---
@router.get("/bienvenida/{ip}")
def mostrar_bienvenida(ip: str, user: str = Depends(get_user_or_redirect)):
    """
    Sends a command to the agent on the specified IP to show a welcome video.
    Protected route.
    """
    subprocess.run(["python3", "tools/install.py", ip])
    return RedirectResponse("/", status_code=303)
