from repositories.film_repo import FilmRepository
from fastapi import HTTPException


class FilmService:
    """Logica de negocio para peliculas. Mismo patron que VideogameService."""

    def __init__(self, repo: FilmRepository):
        self.repo = repo

    async def get_all(self) -> list:
        return await self.repo.find_all()

    async def get_by_id(self, id: str) -> dict:
        film = await self.repo.find_by_id(id)
        if not film:
            raise HTTPException(404, f"Pelicula no encontrada: {id}")
        return film

    async def create(self, data: dict) -> dict:
        # Regla: no puede haber dos peliculas con el mismo nombre
        existing = await self.repo.find_by_name(data["nombre"])
        if existing:
            raise HTTPException(409, "La pelicula ya existe")
        data["play"] = False
        data["abierto"] = False
        return await self.repo.create(data)

    async def update(self, id: str, data: dict) -> dict:
        film = await self.repo.update(id, data)
        if not film:
            raise HTTPException(404, f"Pelicula no encontrada: {id}")
        return film

    async def delete(self, id: str) -> bool:
        deleted = await self.repo.delete(id)
        if not deleted:
            raise HTTPException(404, f"Pelicula no encontrada: {id}")
        return True
