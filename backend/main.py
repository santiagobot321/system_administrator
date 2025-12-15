from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from backend.session import get_user_or_redirect
from backend.routes import auth, equipos, actions, reports
import os

app = FastAPI()

# --- Static Files and Templates ---
# Construct the absolute path to the frontend directory
# This makes the app more robust, as it doesn't depend on the current working directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "frontend/static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "frontend/templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# --- Middleware ---
@app.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    """
    Middleware to add cache-control headers to responses.
    This prevents the browser from caching protected pages, which could allow
    access via the "back" button after logging out.
    """
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# --- Main Application Routes ---

@app.get("/reportes", response_class=HTMLResponse)
async def reportes_page(request: Request, user: str = Depends(get_user_or_redirect)):
    """
    Displays the reports page. Protected route.
    """
    return templates.TemplateResponse("reportes.html", {"request": request, "user_email": user})

# --- Include Routers ---
# The main router for CRUD operations on computers is included with a prefix.
app.include_router(equipos.router, prefix="/equipos", tags=["equipos"])
# The router for remote actions on computers.
app.include_router(actions.router, prefix="/actions", tags=["actions"])
# The router for agent reports.
app.include_router(reports.router, prefix="/reports", tags=["reports"])
# The router for authentication.
app.include_router(auth.router, tags=["authentication"])

# The root path now redirects to the main equipment dashboard.
@app.get("/")
async def root():
    return RedirectResponse(url="/equipos/")
