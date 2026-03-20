from repositories.base import BaseRepository
from typing import Optional


class VideogameRepository(BaseRepository):
    """
    Hereda todo el CRUD del BaseRepository y añade
    queries especificas que solo tienen sentido para videojuegos.
    """

    async def find_by_name_and_console(self, nombre: str, consola: str) -> Optional[dict]:
        """Busca un juego por nombre+consola. Se usa para evitar duplicados."""
        doc = await self.collection.find_one({"nombre": nombre, "consola": consola})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def get_consoles(self) -> list[str]:
        """Devuelve lista de consolas unicas (como SELECT DISTINCT en SQL)."""
        return await self.collection.distinct("consola")

    async def get_by_console(self, consola: str) -> list:
        """Todos los juegos de una consola concreta."""
        return await self.find_all({"consola": consola})

    async def get_playing(self) -> Optional[dict]:
        """Devuelve el juego que tiene play=True (solo puede haber uno)."""
        doc = await self.collection.find_one({"play": True})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def is_any_playing(self) -> bool:
        """True si hay algun juego reproduciendose ahora mismo."""
        doc = await self.collection.find_one({"play": True})
        return doc is not None

    async def set_play(self, nombre: str, consola: str) -> Optional[dict]:
        """Marca un juego como en reproduccion (play=True)."""
        result = await self.collection.find_one_and_update(
            {"nombre": nombre, "consola": consola},
            {"$set": {"play": True}},
            return_document=True
        )
        if result:
            result["_id"] = str(result["_id"])
        return result

    async def set_opened(self, nombre: str, consola: str) -> Optional[dict]:
        """Marca un juego como abierto (el emulador ya lo cargo)."""
        result = await self.collection.find_one_and_update(
            {"nombre": nombre, "consola": consola},
            {"$set": {"abierto": True}},
            return_document=True
        )
        if result:
            result["_id"] = str(result["_id"])
        return result

    async def reset_all(self) -> int:
        """Resetea todos los juegos: play=False, abierto=False."""
        result = await self.collection.update_many(
            {},
            {"$set": {"play": False, "abierto": False}}
        )
        return result.modified_count

    async def get_random_trailer(self) -> Optional[str]:
        """Devuelve la ruta de un trailer aleatorio de entre los que tienen trailer."""
        pipeline = [
            {"$match": {"trailer": {"$exists": True, "$ne": ""}}},
            {"$sample": {"size": 1}}
        ]
        results = await self.collection.aggregate(pipeline).to_list(length=1)
        return results[0]["trailer"] if results else None
