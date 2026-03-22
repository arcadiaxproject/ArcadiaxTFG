from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes import videogames, films, playback, example  # Añadimos la referencia al nuevo módulo example

app = FastAPI(title="ArcadiaX API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videogames.router)
app.include_router(films.router)
app.include_router(playback.router)
app.include_router(example.router)  # Incluimos el nuevo router example

@app.get("/health")
async def health():
    return {"status": "ok", "service": "arcadiax-backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.BACKEND_HOST, port=settings.BACKEND_PORT, reload=True)
