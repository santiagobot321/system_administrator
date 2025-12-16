import os
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

# --- Importamos TODAS las rutas y la lógica de sesión ---
from .routes import auth, equipos, actions, reports, notifications
from .session import get_user_or_redirect  # <-- Importamos la función correcta

# --- Creamos la App FastAPI ---
app = FastAPI()

# --- Configuración de Plantillas y Archivos Estáticos ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend/static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend/templates"))

# --- Middleware ---
@app.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

# --- Endpoints de Páginas HTML ---

@app.get("/attendee", response_class=HTMLResponse)
async def get_attendee_page(request: Request):
    """ Sirve la página para los móviles de los asistentes. """
    return templates.TemplateResponse("attendee.html", {"request": request})

@app.get("/attack", response_class=HTMLResponse)
def get_attacker_console(request: Request, user: str = Depends(get_user_or_redirect)):
    """ Sirve el panel del atacante, protegido por la sesión de usuario. """
    return templates.TemplateResponse("attacker.html", {"request": request})


# --- Incluir TODOS los Routers del Backend ---
app.include_router(auth.router, tags=["Authentication"])
app.include_router(equipos.router, prefix="/equipos", tags=["Equipos"])
app.include_router(actions.router, prefix="/actions", tags=["Actions"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(notifications.router, tags=["Notifications"])

# --- Redirección Raíz ---
@app.get("/", response_class=RedirectResponse)
async def root():
    """ Redirige la raíz al dashboard principal de equipos. """
    # Como el dashboard de equipos está en /equipos/, redirigimos ahí.
    # La ruta /equipos/ a su vez está protegida por get_user_or_redirect.
    return RedirectResponse(url="/equipos/")
