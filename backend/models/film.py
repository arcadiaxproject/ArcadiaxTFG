from pydantic import BaseModel, Field
from typing import Optional


class FilmCreate(BaseModel):
    nombre: str
    ubicacion: str = ""
    trailer: str = ""
    imagen: str = ""


class FilmUpdate(BaseModel):
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    trailer: Optional[str] = None
    imagen: Optional[str] = None


class FilmResponse(BaseModel):
    id: str = Field(alias="_id")
    nombre: str
    ubicacion: str = ""
    trailer: str = ""
    imagen: str = ""
    play: bool = False
    abierto: bool = False

    class Config:
        populate_by_name = True
