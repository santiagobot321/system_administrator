from fastapi import APIRouter
from backend.models import EstadoEquipo, ErrorReport

router = APIRouter()

@router.post("/report")
def recibir_estado(estado: EstadoEquipo):
    """
    SIMULACIÓN para la demo.
    Recibe un reporte de estado, lo imprime en el log del servidor y devuelve éxito.
    No usa base de datos.
    """
    print(f"DEMO: Estado recibido del agente {estado.hostname}: Red={estado.red}, Internet={estado.internet}")
    # En una aplicación real, esto actualizaría la base de datos.
    # Aquí, simplemente confirmamos que la ruta funciona.
    return {"msg": "Estado recibido"}

@router.post("/error")
def recibir_error(error: ErrorReport):
    """
    SIMULACIÓN para la demo.
    Recibe un reporte de error, lo imprime en el log del servidor y devuelve éxito.
    No usa base de datos.
    """
    print(f"DEMO: Error recibido del agente {error.hostname}: {error.error}")
    # En una aplicación real, esto actualizaría la base de datos.
    # Aquí, simplemente confirmamos que la ruta funciona.
    return {"msg": "Error recibido"}
