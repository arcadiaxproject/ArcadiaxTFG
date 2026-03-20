from fastapi import APIRouter, Depends
from services.playback_service import PlaybackService
from dependencies import get_playback_service

router = APIRouter(prefix="/playback", tags=["playback"])


@router.post("/game/{nombre}/{consola}")
async def play_game(nombre: str, consola: str,
                    service: PlaybackService = Depends(get_playback_service)):
    """POST /playback/game/Crash/ps1 — Iniciar un juego."""
    return await service.play_game(nombre, consola)


@router.post("/film/{nombre}")
async def play_film(nombre: str,
                    service: PlaybackService = Depends(get_playback_service)):
    """POST /playback/film/Inception — Iniciar una pelicula."""
    return await service.play_film(nombre)


@router.post("/stop")
async def stop(service: PlaybackService = Depends(get_playback_service)):
    """POST /playback/stop — Parar toda la reproduccion."""
    await service.stop()
    return {"status": "stopped"}


@router.get("/current")
async def current(service: PlaybackService = Depends(get_playback_service)):
    """GET /playback/current — Que se esta reproduciendo ahora."""
    return await service.get_current()


@router.get("/trailer")
async def random_trailer(service: PlaybackService = Depends(get_playback_service)):
    """GET /playback/trailer — Trailer aleatorio."""
    return await service.get_random_trailer()
