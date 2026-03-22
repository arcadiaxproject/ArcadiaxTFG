# Asumiendo que el archivo __init__.py ya existe y contiene la configuración para incluir todas las rutas
from .hola import router as hola_router

__all__ = [
    "hola_router",
]
