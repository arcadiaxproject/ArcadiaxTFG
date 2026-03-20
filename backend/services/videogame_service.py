from repositories.videogame_repo import VideogameRepository
from fastapi import HTTPException


class VideogameService:
    """
    Logica de negocio para videojuegos.
    Las reglas del sistema viven aqui, no en las rutas ni en los repositories.
    """

    def __init__(self, repo: VideogameRepository):
        self.repo = repo

    async def get_all(self) -> list:
        return await self.repo.find_all()

    async def get_by_id(self, id: str) -> dict:
        game = await self.repo.find_by_id(id)
        if not game:
            raise HTTPException(404, f"Videojuego no encontrado: {id}")
        return game

    async def get_consoles(self) -> list[str]:
        consoles = await self.repo.get_consoles()
        if not consoles:
            raise HTTPException(404, "No se encontraron consolas")
        return consoles

    async def get_by_console(self, consola: str) -> list:
        games = await self.repo.get_by_console(consola)
        if not games:
            raise HTTPException(404, f"No hay juegos para: {consola}")
        return games

    async def create(self, data: dict) -> dict:
        # Regla: no puede haber dos juegos con el mismo nombre+consola
        existing = await self.repo.find_by_name_and_console(data["nombre"], data["consola"])
        if existing:
            raise HTTPException(409, "El videojuego ya existe")
        data["play"] = False
        data["abierto"] = False
        return await self.repo.create(data)

    async def update(self, id: str, data: dict) -> dict:
        game = await self.repo.update(id, data)
        if not game:
            raise HTTPException(404, f"Videojuego no encontrado: {id}")
        return game

    async def delete(self, id: str) -> bool:
        deleted = await self.repo.delete(id)
        if not deleted:
            raise HTTPException(404, f"Videojuego no encontrado: {id}")
        return True
