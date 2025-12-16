from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.session import create_session, clear_session
import os

router = APIRouter()

# Apuntamos a la carpeta `frontend` que está en la raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATES_DIR = os.path.join(BASE_DIR, "frontend/templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    """ Sirve la página de login. """
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=RedirectResponse)
async def login_post(email: str = Form(...), password: str = Form(...)):
    """
    Simulación de login para la demo.
    Acepta cualquier email/contraseña y redirige al dashboard.
    No necesita base de datos.
    """
    print(f"DEMO LOGIN: User '{email}' logged in.")
    # Redirige al dashboard principal en /equipos/
    response = RedirectResponse(url="/", status_code=303)
    create_session(response, user_email=email)
    return response

@router.get("/logout", response_class=RedirectResponse)
async def logout():
    """ Cierra la sesión y redirige a la página de login. """
    response = RedirectResponse(url="/login")
    clear_session(response)
    return response
