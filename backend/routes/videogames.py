from fastapi import APIRouter, Depends
from models.Videogame import VideogameCreate, VideogameUpdate, VideogameResponse
from services.videogame_service import VideogameService
from dependencies import get_videogame_service

router = APIRouter(prefix="/videogames", tags=["videogames"])


@router.get("/", response_model=list[VideogameResponse])
async def get_all(service: VideogameService = Depends(get_videogame_service)):
    """GET /videogames — Todos los videojuegos."""
    return await service.get_all()


@router.get("/consoles", response_model=list[str])
async def get_consoles(service: VideogameService = Depends(get_videogame_service)):
    """GET /videogames/consoles — Lista de consolas unicas."""
    return await service.get_consoles()


@router.get("/console/{consola}", response_model=list[VideogameResponse])
async def get_by_console(consola: str, service: VideogameService = Depends(get_videogame_service)):
    """GET /videogames/console/ps1 — Juegos de una consola."""
    return await service.get_by_console(consola)


@router.get("/{id}", response_model=VideogameResponse)
async def get_by_id(id: str, service: VideogameService = Depends(get_videogame_service)):
    """GET /videogames/{id} — Un juego por ID."""
    return await service.get_by_id(id)


@router.post("/", response_model=VideogameResponse, status_code=201)
async def create(game: VideogameCreate, service: VideogameService = Depends(get_videogame_service)):
    """POST /videogames — Crear un juego nuevo."""
    return await service.create(game.model_dump())


@router.put("/{id}", response_model=VideogameResponse)
async def update(id: str, game: VideogameUpdate, service: VideogameService = Depends(get_videogame_service)):
    """PUT /videogames/{id} — Actualizar un juego."""
    return await service.update(id, game.model_dump(exclude_none=True))


@router.delete("/{id}")
async def delete(id: str, service: VideogameService = Depends(get_videogame_service)):
    """DELETE /videogames/{id} — Eliminar un juego."""
    await service.delete(id)
    return {"detail": "Videojuego eliminado"}
