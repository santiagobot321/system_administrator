from fastapi import FastAPI, Request, Form, Depends
from backend.routes import equipos
from backend.database import get_db_connection
from backend.auth import verify_password
from backend.session import create_session, get_current_user, clear_session, get_user_or_redirect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from tools.wol import send_wol

app = FastAPI()
app.mount("/static", StaticFiles(directory="backend/templates/static"), name="static")
# Plantillas HTML
templates = Jinja2Templates(directory="backend/templates")

@app.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    """
    Middleware para añadir cabeceras de control de caché a las respuestas.
    Esto evita que el navegador guarde páginas protegidas y permita el acceso
    con el botón "atrás" después de cerrar sesión.
    """
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    error = request.query_params.get("error")
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.post("/login", response_class=RedirectResponse)
async def login_post(email: str = Form(...), password: str = Form(...)):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
        user_data = cur.fetchone()

        if not user_data or not user_data[0]:
            return RedirectResponse(url="/login?error=1", status_code=303)

        # El conector de la BD puede devolver bytes, passlib espera una cadena.
        hashed_password = user_data[0].decode('utf-8') if isinstance(user_data[0], bytes) else user_data[0]

        if not verify_password(password, hashed_password):
            return RedirectResponse(url="/login?error=1", status_code=303)

        # Si todo es correcto, crea la sesión y redirige a la página principal.
        response = RedirectResponse(url="/", status_code=303)
        create_session(response, user_email=email)
        return response
    finally:
        if conn:
            conn.close()

@app.get("/logout", response_class=RedirectResponse)
async def logout():
    # Limpiamos la cookie de sesión y redirigimos al login.
    response = RedirectResponse(url="/login")
    clear_session(response)
    return response

@app.get("/reportes", response_class=HTMLResponse)
async def reportes(request: Request, user: str = Depends(get_user_or_redirect)):
    # La dependencia 'get_user_or_redirect' ya protege esta ruta.
    # Si el código llega aquí, el usuario está autenticado.
    return templates.TemplateResponse("reportes.html", {"request": request, "user_email": user})





@app.get("/encender/{mac}")
async def encender_equipo(mac: str):
    try:
        send_wol(mac)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return HTMLResponse(content=f"Error al encender el equipo: {e}", status_code=500)



# Incluir las rutas
app.include_router(equipos.router)
