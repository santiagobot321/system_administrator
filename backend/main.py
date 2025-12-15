from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from backend.session import get_user_or_redirect
from backend.routes import auth, equipos, actions, reports, notifications
import os

app = FastAPI()

# --- Static Files and Templates ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "frontend/static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "frontend/templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# --- Middleware ---
@app.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# --- Main Application Routes ---

@app.get("/reportes", response_class=HTMLResponse)
async def reportes_page(request: Request, user: str = Depends(get_user_or_redirect)):
    return templates.TemplateResponse("reportes.html", {"request": request, "user_email": user})

@app.get("/attendee", response_class=HTMLResponse)
async def attendee_page(request: Request):
    """ Serves the page for attendees to connect via QR code. """
    return templates.TemplateResponse("attendee.html", {"request": request})

@app.get("/attacker-console", response_class=HTMLResponse)
async def attacker_page(request: Request, user: str = Depends(get_user_or_redirect)):
    """ Serves the secret attacker's console. """
    return templates.TemplateResponse("attacker.html", {"request": request})


# --- Include Routers ---
app.include_router(equipos.router, prefix="/equipos", tags=["equipos"])
app.include_router(actions.router, prefix="/actions", tags=["actions"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(auth.router, tags=["authentication"])
app.include_router(notifications.router)


# The root path now redirects to the main equipment dashboard.
@app.get("/")
async def root():
    return RedirectResponse(url="/equipos/")
