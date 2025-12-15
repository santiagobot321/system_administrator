from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.database import get_db_connection
from backend.session import get_user_or_redirect
import os

router = APIRouter()

# Construct the absolute path to the templates directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATES_DIR = os.path.join(BASE_DIR, "frontend/templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


# --- List Computers ---
@router.get("/", response_class=HTMLResponse)
def listar_equipos(request: Request, user: str = Depends(get_user_or_redirect)):
    """
    Displays the main dashboard page, listing all computers from the database.
    This route is protected and requires the user to be logged in.
    """
    conn = get_db_connection()
    # Use a dictionary cursor for easier access to columns by name in the template
    cur = conn.cursor(dictionary=True)
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
    user: str = Depends(get_user_or_redirect)
):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Use %s for parameter markers with MariaDB
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
    Protected route.
    """
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Use %s for parameter markers with MariaDB
        cur.execute("DELETE FROM equipos WHERE id=%s", (id,))
        conn.commit()
    finally:
        if conn:
            conn.close()
    return RedirectResponse(url="/equipos/", status_code=303)
