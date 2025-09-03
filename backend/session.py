from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
import os

# --- Session Configuration ---

# IMPORTANT! Change this to a long, random, and secret string for production.
# You can generate one with: python -c 'import secrets; print(secrets.token_hex(32))'
# It's recommended to load this from an environment variable.
SECRET_KEY = os.environ.get("SECRET_KEY", "una-clave-secreta-muy-insegura-cambiar-en-produccion")

# Serializer to sign and verify session cookies.
# It uses the SECRET_KEY to create a cryptographic signature, ensuring that the
# cookie data has not been tampered with.
serializer = URLSafeTimedSerializer(SECRET_KEY)

# The name of the cookie that will store the session token.
SESSION_COOKIE_NAME = "session_token"

def create_session(response: Response, user_email: str):
    """Creates a session token containing user data and sets it in an HTTP-only cookie."""
    # Serialize the user's email into a signed, timestamped string.
    session_data = serializer.dumps({"email": user_email})
    # Set the cookie on the user's browser.
    # httponly=True prevents JavaScript from accessing the cookie, mitigating XSS attacks.
    response.set_cookie(key=SESSION_COOKIE_NAME, value=session_data, httponly=True)

def get_current_user(request: Request) -> str | None:
    """
    Gets the user's email from the session cookie, if the cookie is present and valid.
    Returns the email or None if the session is invalid or expired.
    """
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        return None
    try:
        # Deserialize and verify the token.
        # The max_age of 3600 seconds (1 hour) ensures that the session expires.
        # If the token is older than this, a SignatureExpired exception is raised.
        data = serializer.loads(token, max_age=3600)
        return data.get("email")
    except (SignatureExpired, BadTimeSignature):
        # If the signature is invalid (tampered with) or has expired, return None.
        return None

def clear_session(response: Response):
    """Deletes the session cookie from the user's browser, effectively logging them out."""
    response.delete_cookie(key=SESSION_COOKIE_NAME)

# --- Authentication Dependency ---
async def get_user_or_redirect(request: Request):
    """
    A FastAPI dependency that protects routes.
    It verifies the current user's session. If the session is invalid or non-existent,
    it redirects the user to the login page. Otherwise, it returns the user's email.
    """
    user_email = get_current_user(request)
    if user_email is None:
        # If no valid user is found, issue a redirect to the login page.
        return RedirectResponse(url="/login")
    # If a valid user is found, the request proceeds, and the user's email is available
    # to the path operation function.
    return user_email
