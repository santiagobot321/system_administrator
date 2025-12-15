from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from backend.database import get_db_connection
from backend.session import get_user_or_redirect
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATES_DIR = os.path.join(BASE_DIR, "frontend/templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


# --- HTML Page Route ---
@router.get("/", response_class=HTMLResponse)
def listar_equipos_page(request: Request, user: str = Depends(get_user_or_redirect)):
    """
    Displays the main dashboard page, listing all computers from the database.
    """
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, hostname, mac, ip, estado, conectado, error FROM equipos")
    equipos = cur.fetchall()
    conn.close()
    return templates.TemplateResponse("base.html", {"request": request, "equipos": equipos})

# --- API Data Route ---
@router.get("/api/equipos", response_class=JSONResponse)
def listar_equipos_api(user: str = Depends(get_user_or_redirect)):
    """
    Returns a JSON list of all computers. This is used by the attacker's panel.
    """
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, hostname, ip FROM equipos")
    equipos = cur.fetchall()
    conn.close()
    return equipos


# --- Add Computer ---
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
        cur.execute(
            "INSERT INTO equipos (hostname, mac, ip, estado) VALUES (%s, %s, %s, %s)",
            (hostname, mac, ip, estado)
        )
        conn.commit()
    finally:
        if conn:
            conn.close()
    return RedirectResponse(url="/equipos/", status_code=303)

# --- Delete Computer ---
@router.get("/delete/{id}", response_class=RedirectResponse)
async def eliminar_equipo(id: int, user: str = Depends(get_user_or_redirect)):
    """
    Deletes a computer from the database based on its ID.
    """
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM equipos WHERE id=%s", (id,))
        conn.commit()
    finally:
        if conn:
            conn.close()
    return RedirectResponse(url="/equipos/", status_code=303)
