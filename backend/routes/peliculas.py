from database.Peliculas import create_film, get_all_film,get_one_film_name,existe_pelicula_en_play,set_play_true,set_abierto_true,pelicula_ejecucion,resetear_pelicula,obtener_trailer,obtener_pelicula_en_reproduccion,pelicula_ejecutando
from routes.models.Peliculas import Pelicula, UpdatePelicula
from fastapi import HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import List
pelicula=APIRouter()

@pelicula.get("/multimedia/peliculas")
async def get_peliculas():
    peliculas=await get_all_film()
    return peliculas

@pelicula.post("/multimedia/pelicula",response_model= Pelicula)
async def new_pelicula(pelicula:Pelicula):
    film_found=await get_one_film_name(nombre=pelicula.nombre)
    if film_found:
        raise HTTPException(409,"la pelicula ya existe")
    response=await create_film(pelicula.dict())
    return response

@pelicula.put("/multimedia/pelicula/{nombre}",response_model=Pelicula)
async def put_play_true(nombre:str):
    en_ejecucion=await existe_pelicula_en_play()
    if en_ejecucion:
        raise HTTPException(status_code=400, detail="Ya hay una pelcula  en ejecución")
    response=await set_play_true(nombre)
    return response

@pelicula.put("/multimedia/pelicula/abrir/{nombre}",response_model=Pelicula)
async def put_abierto_true(nombre:str):
    response=await set_abierto_true(nombre)
    return response


@pelicula.put("/pelicula/resetear", response_model=bool)
async def put_play_false():
    try:
        # Llama a la función para restablecer todos los videojuegos
        modificados = await resetear_pelicula()
        # Devuelve True si se modificó al menos un videojuego, False si no
        return modificados > 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@pelicula.get("/multimedia/pelicula/trailer",response_model=str)
async def obtener_random_trailer():
    response=await obtener_trailer()
    return response

@pelicula.get("/pelicula/ejecutando",response_model=bool)
async def pelicula_ejecucion():
    response=await pelicula_ejecutando()
    return response

@pelicula.get("/multimedia/pelicula/en-reproduccion",response_model=Pelicula)
async def obtener_pelicula_reproduccion():
    response=await obtener_pelicula_en_reproduccion()
    return response