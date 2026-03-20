from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes.videogames import videojuego
from routes.peliculas import pelicula

from dotenv import load_dotenv
import os

# Cargar variables desde .env
load_dotenv()

# Obtener IP y orígenes permitidos
IP = os.getenv("IP", "127.0.0.1")
FRONTEND_ORIGINS = os.getenv("FRONTEND_ORIGINS", f"http://{IP}:3000,http://localhost:3000").split(",")

app = FastAPI()

# Configuración del middleware CORS con orígenes desde .env
app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videojuego)
app.include_router(pelicula)

# Ejecutar con:python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
