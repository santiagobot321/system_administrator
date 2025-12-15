from fastapi import APIRouter
from backend.models import EstadoEquipo, ErrorReport
from backend.database import get_db_connection

router = APIRouter()

@router.post("/report")
def recibir_estado(estado: EstadoEquipo):
    """
    Receives a status report from a client agent.
    Updates the computer's status, connectivity, and network details in the database.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    status_string = f"Red: {estado.red}, Internet: {estado.internet}"
    is_connected = estado.red and estado.internet
    
    # Use %s for parameter markers, which is correct for MariaDB.
    cur.execute(
        "UPDATE equipos SET estado=%s, conectado=%s WHERE hostname=%s",
        (status_string, is_connected, estado.hostname)
    )
    conn.commit()
    conn.close()
    return {"msg": "Estado recibido"}

@router.post("/error")
def recibir_error(error: ErrorReport):
    """
    Receives an error report from a client agent.
    Updates the computer's error field in the database.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE equipos SET error=%s WHERE hostname=%s",
        (error.error, error.hostname)
    )
    conn.commit()
    conn.close()
    return {"msg": "Error recibido"}
