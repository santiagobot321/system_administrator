from pydantic import BaseModel

# Pydantic model for validating the payload from an agent's status report.
class EstadoEquipo(BaseModel):
    hostname: str
    ip: str
    red: bool
    internet: bool

# Pydantic model for validating the payload from an agent's error report.
class ErrorReport(BaseModel):
    hostname: str
    error: str
