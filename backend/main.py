# Asumiendo que el archivo main.py ya existe y contiene la configuración del FastAPI
from fastapi import FastAPI
from backend.routes.hola import router as hola_router

app = FastAPI()

# Incluir las rutas adicionales
app.include_router(hola_router, tags=["Hola"])
