from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import Optional


# CRUD generico: Cualquier entidad nueva hereda de aqui y obtiene
# find_all, find_by_id, create, update y delete automaticamente.
class BaseRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def find_all(self, filtro: dict = None) -> list:
        cursor = self.collection.find(filtro or {})
        docs = await cursor.to_list(length=500)
        for doc in docs:
            doc["_id"] = str(doc["_id"])  # ObjectId → string para que JSON lo entienda
        return docs

    async def find_by_id(self, id: str) -> Optional[dict]:
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def create(self, data: dict) -> dict:
        result = await self.collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data

    async def update(self, id: str, data: dict) -> Optional[dict]:
        # Filtramos los campos None para no sobreescribir datos existentes
        update_data = {k: v for k, v in data.items() if v is not None}
        if not update_data:
            return await self.find_by_id(id)
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_data},
            return_document=True  # Devuelve el documento ya actualizado
        )
        if result:
            result["_id"] = str(result["_id"])
        return result

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
