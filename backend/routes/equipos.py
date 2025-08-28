from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.database import get_db_connection
from backend.session import get_user_or_redirect
from tools.wol import send_wol

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

# --- Listar equipos ---
@router.get("/", response_class=HTMLResponse)
async def listar_equipos(request: Request, user: str = Depends(get_user_or_redirect)):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, hostname, mac, ip, estado FROM equipos")
        equipos = cur.fetchall()
    finally:
        if conn:
            conn.close()
    return templates.TemplateResponse("base.html", {"request": request, "equipos": equipos, "user_email": user})

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
@router.get("/apagar/{ip}", response_class=RedirectResponse)
async def apagar_equipo(ip: str, user: str = Depends(get_user_or_redirect)):
    # Aquí iría la lógica para apagar el equipo, por ejemplo, usando SSH.
    # subprocess.run(["ssh", f"usuario@{ip}", "sudo poweroff"])
    print(f"Solicitud para apagar el equipo en la IP: {ip}")
    return RedirectResponse(url="/", status_code=303)
