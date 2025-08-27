from fastapi import FastAPI, Request, Form
from backend.routes import equipos
from backend.database import get_db_connection
from backend.auth import verify_password
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse


app = FastAPI()

app.mount("/static", StaticFiles(directory="backend/templates/static"), name="static")
# Plantillas HTML
templates = Jinja2Templates(directory="backend/templates")

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

        # Si el usuario no existe o la contraseña es incorrecta, redirige con error.
        if not user_data:
            return RedirectResponse(url="/login?error=1", status_code=303)

        raw_hash = user_data[0]

        # Si el usuario no existe o el hash es nulo, redirige con error.
        if not raw_hash:
            return RedirectResponse(url="/login?error=1", status_code=303)

        # El conector de la BD puede devolver bytes, passlib espera una cadena.
        hashed_password = raw_hash.decode('utf-8') if isinstance(raw_hash, bytes) else raw_hash

        if not verify_password(password, hashed_password):
            return RedirectResponse(url="/login?error=1", status_code=303)

        # Si todo es correcto, redirige a reportes.
        return RedirectResponse(url="/reportes", status_code=303)
    finally:
        if conn:
            conn.close()

@app.get("/logout", response_class=RedirectResponse)
async def logout():
    # En una aplicación real, aquí limpiarías la sesión del usuario.
    return RedirectResponse(url="/login")

@app.get("/reportes", response_class=HTMLResponse)
async def reportes(request: Request):
    return templates.TemplateResponse("reportes.html", {"request": request})
# Incluir las rutas
app.include_router(equipos.router)
