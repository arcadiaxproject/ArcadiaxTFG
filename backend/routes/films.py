from fastapi import APIRouter, Depends
from models.film import FilmCreate, FilmResponse
from services.film_service import FilmService
from dependencies import get_film_service

router = APIRouter(prefix="/films", tags=["films"])


@router.get("/", response_model=list[FilmResponse])
async def get_all(service: FilmService = Depends(get_film_service)):
    """GET /films — Todas las peliculas."""
    return await service.get_all()


@router.get("/{id}", response_model=FilmResponse)
async def get_by_id(id: str, service: FilmService = Depends(get_film_service)):
    """GET /films/{id} — Una pelicula por ID."""
    return await service.get_by_id(id)


@router.post("/", response_model=FilmResponse, status_code=201)
async def create(film: FilmCreate, service: FilmService = Depends(get_film_service)):
    """POST /films — Crear una pelicula."""
    return await service.create(film.model_dump())


@router.delete("/{id}")
async def delete(id: str, service: FilmService = Depends(get_film_service)):
    """DELETE /films/{id} — Eliminar una pelicula."""
    await service.delete(id)
    return {"detail": "Pelicula eliminada"}
