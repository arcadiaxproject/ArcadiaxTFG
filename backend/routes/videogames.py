from database.Videojuego import get_all_videogame,create_videogame,get_one_videogame_nombre_consola,get_one_videogame_id,delete_videogame,update_videogame, obtener_consolas,obtener_juegos_por_consola,set_play_true,existe_videogame_en_play,resetear_videogames,obtener_consola_historia
from routes.models.Videojuego import Videogame,UpdateVideogame
from fastapi import HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from database.Videojuego import collection
from typing import Union
videojuego=APIRouter()

#CRUD BASICO

@videojuego.get("/arcade/videojuegos")
async def get_videojuegos():
    videogames=await get_all_videogame()
    return videogames

@videojuego.post("/arcade/videojuego",response_model=Videogame)
async def new_videojuego(videojuego:Videogame):
    videogame_found=await get_one_videogame_nombre_consola(nombre=videojuego.nombre, consola=videojuego.consola)
    if videogame_found:
        raise HTTPException(409,"videojuego ya existe")
    response=await create_videogame(videojuego.dict())
    if response:
        return response
    raise HTTPException(400, "No se pudo guardar el videojuego")

@videojuego.get("/arcade/videojuego/{id}", response_model=Videogame)
async def get_videojuego(id: str):
    videogame = await get_one_videogame_id(id)
    if videogame:
        return videogame
    raise HTTPException(status_code=404, detail=f"Videojuego no encontrado con id {id}")

@videojuego.put("/arcade/videojuego/{id}",response_model=Videogame)
async def put_videogame(id:str,videogame:UpdateVideogame):
   response=await  update_videogame(id, videogame)
   if response:
       return response
   raise HTTPException(status_code=404, detail=f"Videojuego no encontrado con id {id}")

@videojuego.delete("/arcade/videojuego/{id}")
async def remove_videojuego(id:str):
    response=await delete_videogame(id)
    if response:
        return "Videojuego eliminado"
    raise HTTPException(status_code=404, detail=f"Videojuego no encontrado con id {id}")




@videojuego.get("/arcade/consolas", response_model=list[str])
async def get_consolas():
    consolas = await obtener_consolas()
    if consolas:
        return consolas
    raise HTTPException(status_code=404, detail="No se encontraron consolas")

@videojuego.get("/consolas/historia", response_model=Union[str, dict])
async def get_consolas_competitivo():
    consolas = await obtener_consola_historia()
    if consolas:
        return consolas
    raise HTTPException(status_code=404, detail="No se encontraron consolas en modo historia")

@videojuego.get("/arcade/juegos/{consola}", response_model=List[Videogame])
async def get_juegos_por_consola(consola: str):
    try:
        # Llama a la función para obtener los juegos de la consola especificada
        juegos = await obtener_juegos_por_consola(consola)
        if not juegos:
            raise HTTPException(status_code=404, detail=f"No se encontraron juegos para la consola {consola}")
        return juegos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import HTTPException

from fastapi import HTTPException

@videojuego.put("/arcade/videojuego/{nombre}/{consola}", response_model=Videogame)
async def put_play_true(nombre: str, consola: str):
    # Verificamos si ya hay un videojuego en ejecución
    en_ejecucion = await existe_videogame_en_play()
    
    if en_ejecucion:
        raise HTTPException(status_code=400, detail="Ya hay un videojuego en ejecución")

    # Llamamos a la función para actualizar el campo 'play' a true
    response = await set_play_true(nombre, consola)
    
    if response:
        return response
    
    raise HTTPException(status_code=404, detail=f"Videojuego no encontrado con nombre '{nombre}' y consola '{consola}'")
@videojuego.put("/arcade/reset", response_model=bool)
async def put_play_false():
    """
    Resetea todos los videojuegos estableciendo 'play' y 'reproduciendo' a False.
    Devuelve True si se modificó al menos un videojuego, de lo contrario False.
    """
    try:
        # Llama a la función para restablecer todos los videojuegos
        modificados = await resetear_videogames()
        # Devuelve True si se modificó al menos un videojuego, False si no
        return modificados > 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Devuelve TRUE o FALSE ante la pregunta ¿hay algun videojuego play==True?
@videojuego.get("/arcade/juego/ejecutando", response_model=bool)
async def videojuego_ejecutando():
    """
    Devuelve True si hay un videojuego en reproducción (play=True).
    Devuelve False si no hay ningún videojuego en reproducción.
    """
    try:
        videojuego = await collection.find_one({"play": True})
        return videojuego is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al verificar el estado del videojuego: {str(e)}")
#Devuelve la informacion del juego play

@videojuego.get("/arcade/juego/en-reproduccion", response_model=Videogame)
async def obtener_videojuego_en_reproduccion():
    """
    Devuelve la información del videojuego cuyo campo 'play' está en True.
    Si no hay ningún videojuego en reproducción, devuelve un error 404.
    """
    try:
        # Busca un videojuego en la colección donde 'play' sea True
        videojuego = await collection.find_one({"play": True})

        # Si no encuentra un videojuego, devuelve error 404
        if not videojuego:
            raise HTTPException(status_code=404, detail="No hay ningún videojuego en reproducción")

        # Convierte el '_id' a string para evitar problemas al devolver el resultado
        videojuego["_id"] = str(videojuego["_id"])

        return videojuego
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los datos del videojuego: {str(e)}")

#Pone abierto a true a traves del nombre y de la consola
@videojuego.put("/arcade/juego/abrir/{nombre}/{consola}", response_model=Videogame)
async def poner_abierto_true(nombre: str, consola: str):
    """
    Actualiza el campo 'abierto' a True para el videojuego especificado por 'nombre' y 'consola'.
    Si no encuentra el videojuego, devuelve un error 404.
    """
    try:
        # Busca y actualiza el videojuego con 'nombre' y 'consola' proporcionados
        resultado = await collection.find_one_and_update(
            {"nombre": nombre, "consola": consola},
            {"$set": {"abierto": True}},
            return_document=True
        )

        # Si no se encuentra el videojuego, devuelve error 404
        if not resultado:
            raise HTTPException(status_code=404, detail=f"Videojuego no encontrado con nombre '{nombre}' y consola '{consola}'")

        # Convierte el '_id' a string para evitar problemas al devolver el resultado
        resultado["_id"] = str(resultado["_id"])

        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el campo 'abierto': {str(e)}")
#obtenemos un tailer random 
@videojuego.get("/arcade/juego/trailer", response_model=str)
async def obtener_trailer_aleatorio():
    """
    Devuelve el tráiler de un videojuego seleccionado aleatoriamente como un string.
    Si no hay ningún videojuego o no tiene tráiler, devuelve un error 404.
    """
    try:
        # Selecciona un videojuego aleatorio utilizando $sample de MongoDB
        pipeline = [{"$sample": {"size": 1}}]
        resultado = await collection.aggregate(pipeline).to_list(length=1)

        # Verifica si se ha encontrado algún videojuego
        if not resultado:
            raise HTTPException(status_code=404, detail="No se encontró ningún videojuego en la base de datos")

        # Extrae el videojuego encontrado
        videojuego = resultado[0]

        # Verifica si el campo 'trailer' existe en el documento
        trailer = videojuego.get("trailer")
        if not trailer:
            raise HTTPException(status_code=404, detail="El videojuego seleccionado no tiene un tráiler disponible")

        # Devuelve el tráiler como string
        return trailer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el tráiler aleatorio: {str(e)}")
