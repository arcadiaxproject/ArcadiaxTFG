from repositories.base import BaseRepository
from typing import Optional


class FilmRepository(BaseRepository):
    """
    Hereda todo el CRUD del BaseRepository y añade
    queries especificas para peliculas.
    """

    async def find_by_name(self, nombre: str) -> Optional[dict]:
        """Busca una pelicula por nombre. Se usa para evitar duplicados."""
        doc = await self.collection.find_one({"nombre": nombre})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def get_playing(self) -> Optional[dict]:
        """Devuelve la pelicula que tiene play=True."""
        doc = await self.collection.find_one({"play": True})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def is_any_playing(self) -> bool:
        """True si hay alguna pelicula reproduciendose ahora mismo."""
        doc = await self.collection.find_one({"play": True})
        return doc is not None

    async def set_play(self, nombre: str) -> Optional[dict]:
        """Marca una pelicula como en reproduccion (play=True)."""
        result = await self.collection.find_one_and_update(
            {"nombre": nombre},
            {"$set": {"play": True}},
            return_document=True
        )
        if result:
            result["_id"] = str(result["_id"])
        return result

    async def set_opened(self, nombre: str) -> Optional[dict]:
        """Marca una pelicula como abierta (el reproductor la cargo)."""
        result = await self.collection.find_one_and_update(
            {"nombre": nombre},
            {"$set": {"abierto": True}},
            return_document=True
        )
        if result:
            result["_id"] = str(result["_id"])
        return result

    async def reset_all(self) -> int:
        """Resetea todas las peliculas: play=False, abierto=False."""
        result = await self.collection.update_many(
            {},
            {"$set": {"play": False, "abierto": False}}
        )
        return result.modified_count

    async def get_random_trailer(self) -> Optional[str]:
        """Devuelve la ruta de un trailer aleatorio."""
        pipeline = [
            {"$match": {"trailer": {"$exists": True, "$ne": ""}}},
            {"$sample": {"size": 1}}
        ]
        results = await self.collection.aggregate(pipeline).to_list(length=1)
        return results[0]["trailer"] if results else None
