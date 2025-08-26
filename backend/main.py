from fastapi import FastAPI, Request
from backend.routes import equipos
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


app = FastAPI()

app.mount("/static", StaticFiles(directory="backend/templates/static"), name="static")
# Plantillas HTML
templates = Jinja2Templates(directory="backend/templates")

@app.get("/reportes", response_class=HTMLResponse)
async def reportes(request: Request):
    return templates.TemplateResponse("reportes.html", {"request": request})
# Incluir las rutas
app.include_router(equipos.router)
