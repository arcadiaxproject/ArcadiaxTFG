from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import Optional

#CRUD generico: Cualquier entidad nueva hereda de aqui y obtiene find_all, find_by_id, create, updatte y delete.
class BaseRepository:
    def __init__(self, collection:AsyncIOMotorCollection):
        self.collection=collection


async def find_all(self, filtro:dict=None)-> list:
    cursor=self.collection.find(filtro or  {})
    docs= await cursor.to_list(length=500)
    for doc in docs:
        doc["_id"]=str(doc["_id"])
    return doc