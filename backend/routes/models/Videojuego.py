from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class PyObjectID(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

class Videogame(BaseModel):
    id: Optional[PyObjectID] = Field(default=None, alias="_id")
    nombre: str
    ubicacion: Optional[str] = None
    consola: Optional[str] = None
    imagen: Optional[str] = None
    trailer: Optional[str] = None
    abierto: bool = False
    play: bool = False

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class UpdateVideogame(BaseModel):
    nombre: Optional[str]=None
    ubicacion: Optional[str] = None
    consola: Optional[str] = None
    imagen: Optional[str] = None
    trailer: Optional[str] = None
    abierto: Optional[bool] = None
    play: Optional[bool]= None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
