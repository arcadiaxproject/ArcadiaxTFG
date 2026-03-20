from pydantic import BaseModel, Field
from typing import Optional

class VideogameCreate(BaseModel):
    nombre:str
    consola:str
    ubicacion:str=""
    trailer:str=""
    imagen:str=""

class VideogameUpdate(BaseModel):
    nombre: Optional[str] = None
    consola: Optional[str] = None
    ubicacion: Optional[str] = None
    trailer: Optional[str] = None
    imagen: Optional[str] = None


class VideogameResponse(BaseModel):
    id: str = Field(alias="_id")
    nombre: str
    consola: str
    ubicacion: str = ""
    trailer: str = ""
    imagen: str = ""
    play: bool = False      # ¿Está reproduciéndose ahora?
    abierto: bool = False   # ¿El emulador ya lo ha abierto?

    class Config:
        populate_by_name = True