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
# HTML Templates
templates = Jinja2Templates(directory="backend/templates")

@app.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    """
    Middleware to add cache-control headers to responses.
    This prevents the browser from caching protected pages, which could allow
    access via the "back" button after logging out.
    """
    # Process the request and get the response
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    # Check for an error message in the query parameters to display it on the login page.
    error = request.query_params.get("error")
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.post("/login", response_class=RedirectResponse)
async def login_post(email: str = Form(...), password: str = Form(...)):
    conn = None
    try:
        # Establish a database connection.
        conn = get_db_connection()
        cur = conn.cursor()
        # Fetch the user's hashed password from the database based on the provided email.
        cur.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
        user_data = cur.fetchone()

        # If no user is found or they don't have a password set, redirect to login with an error.
        if not user_data or not user_data[0]:
            return RedirectResponse(url="/login?error=1", status_code=303)

        # The DB connector might return bytes; passlib expects a string. Decode if necessary.
        hashed_password = user_data[0].decode('utf-8') if isinstance(user_data[0], bytes) else user_data[0]

        # Verify the provided plain password against the stored hash.
        if not verify_password(password, hashed_password):
            return RedirectResponse(url="/login?error=1", status_code=303)

        # If everything is correct, create a session and redirect to the main page.
        response = RedirectResponse(url="/", status_code=303)
        create_session(response, user_email=email)
        return response
    finally:
        # Ensure the database connection is closed, even if errors occur.
        if conn:
            conn.close()

@app.get("/logout", response_class=RedirectResponse)
async def logout():
    # Clear the session cookie and redirect to the login page.
    response = RedirectResponse(url="/login")
    clear_session(response)
    return response

@app.get("/reportes", response_class=HTMLResponse)
async def reportes(request: Request, user: str = Depends(get_user_or_redirect)):
    # The 'get_user_or_redirect' dependency already protects this route.
    # If the code reaches this point, the user is authenticated.
    return templates.TemplateResponse("reportes.html", {"request": request, "user_email": user})





@app.get("/encender/{mac}")
async def encender_equipo(mac: str):
    try:
        # Send the Wake-on-LAN magic packet to the specified MAC address.
        send_wol(mac)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        # Return an error response if something goes wrong.
        return HTMLResponse(content=f"Error al encender el equipo: {e}", status_code=500)



# Include the routers from other modules.
app.include_router(equipos.router)
