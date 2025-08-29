from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
import os

# --- Configuración de Sesión ---

# ¡IMPORTANTE! Cambia esto por una cadena de caracteres larga, aleatoria y secreta.
# Puedes generar una con: python -c 'import secrets; print(secrets.token_hex(32))'
SECRET_KEY = os.environ.get("SECRET_KEY", "una-clave-secreta-muy-insegura-cambiar-en-produccion")

# Serializador para firmar y verificar las cookies de sesión
serializer = URLSafeTimedSerializer(SECRET_KEY)

SESSION_COOKIE_NAME = "session_token"

def create_session(response: Response, user_email: str):
    """Crea un token de sesión y lo establece en una cookie."""
    session_data = serializer.dumps({"email": user_email})
    response.set_cookie(key=SESSION_COOKIE_NAME, value=session_data, httponly=True)

def get_current_user(request: Request) -> str | None:
    """Obtiene el email del usuario desde la cookie de sesión, si es válida."""
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        return None
    try:
        # El max_age de 3600 segundos (1 hora) asegura que la sesión expire.
        data = serializer.loads(token, max_age=3600)
        return data.get("email")
    except (SignatureExpired, BadTimeSignature):
        return None

def clear_session(response: Response):
    """Elimina la cookie de sesión."""
    response.delete_cookie(key=SESSION_COOKIE_NAME)

# --- Dependencia de autenticación ---
async def get_user_or_redirect(request: Request):
    """Dependencia que verifica la sesión y redirige al login si no es válida."""
    user_email = get_current_user(request)
    if user_email is None:
        return RedirectResponse(url="/login")
    return user_email