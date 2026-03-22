from fastapi import FastAPI
from backend.api.ping import router as ping_router

app = FastAPI()

# Incluir el router de ping
app.include_router(ping_router, prefix="", tags=["ping"])

# Resto del código existente en main.py (si lo hay) debería ir aquí.
