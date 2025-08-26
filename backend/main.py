from fastapi import FastAPI
from backend.routes import equipos

app = FastAPI()

# Incluir las rutas
app.include_router(equipos.router)
