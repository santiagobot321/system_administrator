from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
import subprocess
import re
from backend.session import get_user_or_redirect
from tools.wol import send_wol

router = APIRouter()

# --- IP Address Validation ---
IP_REGEX = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

def validate_ip(ip: str):
    if not IP_REGEX.match(ip):
        raise HTTPException(status_code=400, detail="Invalid IP address format")
    return ip

# --- Remote Actions ---

@router.get("/encender/{mac}", response_class=RedirectResponse)
async def encender_equipo(mac: str, user: str = Depends(get_user_or_redirect)):
    """
    Sends a Wake-on-LAN (WOL) magic packet to the specified MAC address.
    Protected route.
    """
    try:
        print(f"Sending Magic Packet to MAC: {mac}")
        send_wol(mac)
    except Exception as e:
        print(f"Error trying to turn on computer {mac}: {e}")
    return RedirectResponse(url="/equipos/", status_code=303)

@router.get("/apagar/{ip}")
def apagar_equipo(ip: str = Depends(validate_ip), user: str = Depends(get_user_or_redirect)):
    """
    Sends a shutdown command to the agent on the specified IP.
    Protected and validated route.
    """
    subprocess.run(["python3", "tools/host.py", ip])
    return RedirectResponse(url="/equipos/", status_code=303)

@router.get("/instalar/{ip}")
def instalar_vscode_equipo(ip: str = Depends(validate_ip), user: str = Depends(get_user_or_redirect)):
    """
    Sends a command to the agent to install an application.
    Protected and validated route.
    """
    subprocess.run(["python3", "tools/install.py", ip])
    return RedirectResponse(url="/equipos/", status_code=303)

@router.get("/bienvenida/{ip}")
def mostrar_bienvenida(ip: str = Depends(validate_ip), user: str = Depends(get_user_or_redirect)):
    """
    Sends a command to the agent to show a welcome video.
    Protected and validated route.
    """
    subprocess.run(["python3", "tools/install.py", ip])
    return RedirectResponse(url="/equipos/", status_code=303)
