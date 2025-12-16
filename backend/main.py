import os
from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from typing import List, Dict, Any

# --- Importamos TODAS las rutas del backend ---
from .routes import auth, equipos, actions, reports, notifications

# --- Creamos la App FastAPI ---
app = FastAPI()

# --- Configuración de Plantillas y Archivos Estáticos ---
# Apuntamos a la carpeta `frontend` que está en la raíz del proyecto.
# La ruta se construye subiendo dos niveles desde este archivo (backend/main.py -> backend/ -> raíz)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend/static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend/templates"))

# --- Middleware (Copiado de la versión funcional) ---
@app.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

# --- Endpoints de Páginas HTML ---
# NOTA: La lógica de estas páginas está ahora en sus respectivos routers,
# pero dejamos aquí las que no encajan en otro sitio, como la de los asistentes.

@app.get("/attendee", response_class=HTMLResponse)
async def get_attendee_page(request: Request):
    """ Sirve la página para los móviles de los asistentes. """
    return templates.TemplateResponse("attendee.html", {"request": request})

@app.get("/attack", response_class=HTMLResponse)
def get_attacker_console(request: Request, user: str = Depends(auth.manager.get_current_user)):
    """ Sirve el panel del atacante, protegido por autenticación. """
    return templates.TemplateResponse("attacker.html", {"request": request})


# --- Incluir TODOS los Routers del Backend ---
# Cada router tiene sus propias rutas y lógica.
app.include_router(auth.router, tags=["Authentication"])
app.include_router(equipos.router, prefix="/equipos", tags=["Equipos"])
app.include_router(actions.router, prefix="/actions", tags=["Actions"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(notifications.router, tags=["Notifications"])

# --- Redirección Raíz ---
@app.get("/", response_class=RedirectResponse)
async def root():
    """ Redirige la raíz al dashboard principal de equipos. """
    return RedirectResponse(url="/equipos/")
