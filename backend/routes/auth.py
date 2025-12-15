from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.database import get_db_connection
from backend.auth import verify_password
from backend.session import create_session, clear_session
import os

router = APIRouter()

# Construct the absolute path to the templates directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATES_DIR = os.path.join(BASE_DIR, "frontend/templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    error = request.query_params.get("error")
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@router.post("/login", response_class=RedirectResponse)
async def login_post(email: str = Form(...), password: str = Form(...)):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Use %s for parameter markers with MariaDB
        cur.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
        user_data = cur.fetchone()

        if not user_data or not user_data[0]:
            return RedirectResponse(url="/login?error=1", status_code=303)

        hashed_password = user_data[0].decode('utf-8') if isinstance(user_data[0], bytes) else user_data[0]

        if not verify_password(password, hashed_password):
            return RedirectResponse(url="/login?error=1", status_code=303)

        # Redirect to the main equipment dashboard on successful login
        response = RedirectResponse(url="/equipos/", status_code=303)
        create_session(response, user_email=email)
        return response
    finally:
        if conn:
            conn.close()

@router.get("/logout", response_class=RedirectResponse)
async def logout():
    response = RedirectResponse(url="/login")
    clear_session(response)
    return response
