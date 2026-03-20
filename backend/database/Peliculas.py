from motor.motor_asyncio import AsyncIOMotorClient
from routes.models.Peliculas import Pelicula
from bson import ObjectId
from fastapi import HTTPException

# Configuración del cliente de MongoDB
client = AsyncIOMotorClient("mongodb+srv://javier:javier@cluster0.t5cgbal.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
database = client.multimedia
collection = database.peliculas

# Obtener todas las películas
async def get_all_film():
    films = []
    cursor = collection.find({})
    async for document in cursor:
        films.append(Pelicula(**document))
    return films

# Crear una nueva película
async def create_film(pelicula):
    try:
        new_film = await collection.insert_one(pelicula)
        film_created = await collection.find_one({"_id": new_film.inserted_id})
        return film_created
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la película: {str(e)}")

# Obtener una película por nombre
async def get_one_film_name(nombre: str):
    try:
        pelicula = await collection.find_one({"nombre": nombre})
        if not pelicula:
            raise HTTPException(status_code=404, detail=f"No se encontró ninguna película con el nombre '{nombre}'")
        return pelicula
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar la película: {str(e)}")

# Verificar si existe una película en reproducción (play=True)
async def existe_pelicula_en_play():
    try:
        return await collection.find_one({"play": True}) is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al verificar el estado de reproducción: {str(e)}")

# Establecer play=True para una película específica
async def set_play_true(nombre: str):
    try:
        resultado = await collection.update_one({"nombre": nombre}, {"$set": {"play": True}})
        if resultado.matched_count > 0:
            document = await collection.find_one({"nombre": nombre})
            return document
        else:
            raise HTTPException(status_code=404, detail=f"Película no encontrada con nombre '{nombre}'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el estado de reproducción: {str(e)}")

# Establecer abierto=True para una película específica
async def set_abierto_true(nombre: str):
    try:
        resultado = await collection.update_one({"nombre": nombre}, {"$set": {"abierto": True}})
        if resultado.matched_count > 0:
            document = await collection.find_one({"nombre": nombre})
            return document
        else:
            raise HTTPException(status_code=404, detail=f"Película no encontrada con nombre '{nombre}'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el estado de abierto: {str(e)}")

# Obtener la película en reproducción (play=True)
async def pelicula_ejecucion():
    try:
        pelicula = await collection.find_one({"play": True})
        if not pelicula:
            raise HTTPException(status_code=404, detail="No hay ninguna película en reproducción")
        return pelicula
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la película en reproducción: {str(e)}")

# Resetear todas las películas (play=False, abierto=False)
async def resetear_pelicula():
    try:
        resultado = await collection.update_many(
            {},
            {"$set": {"play": False, "abierto": False}}
        )
        return resultado.modified_count
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resetear las películas: {str(e)}")

# Obtener un tráiler aleatorio
async def obtener_trailer():
    try:
        # Selecciona una película aleatoria utilizando $sample de MongoDB
        pipeline = [{"$sample": {"size": 1}}]
        resultado = await collection.aggregate(pipeline).to_list(length=1)

        # Verifica si se ha encontrado alguna película
        if not resultado:
            raise HTTPException(status_code=404, detail="No se encontró ninguna película en la base de datos")

        # Extrae la película encontrada
        pelicula = resultado[0]

        # Verifica si el campo 'trailer' existe en el documento
        trailer = pelicula.get("trailer")
        if not trailer:
            raise HTTPException(status_code=404, detail="La película seleccionada no tiene un tráiler disponible")

        # Devuelve el tráiler como string
        return trailer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el tráiler aleatorio: {str(e)}")

# Obtener la información de la película en reproducción (play=True)
async def obtener_pelicula_en_reproduccion():
    try:
        pelicula = await collection.find_one({"play": True})
        if not pelicula:
            raise HTTPException(status_code=404, detail="No hay ninguna película en reproducción")
        return pelicula
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los datos de la película: {str(e)}")

async def pelicula_ejecutando():
    try:
        pelicula=await collection.find_one({"play":True})
        return pelicula is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al verificar el estado del videojuego: {str(e)}")
async def obtener_pelicula_en_reproduccion():
    try:
        # Busca un videojuego en la colección donde 'play' sea True
        pelicula = await collection.find_one({"play": True})

        # Si no encuentra un videojuego, devuelve error 404
        if not pelicula:
            raise HTTPException(status_code=404, detail="No hay ningún videojuego en reproducción")

        # Convierte el '_id' a string para evitar problemas al devolver el resultado
        pelicula["_id"] = str(pelicula["_id"])

        return pelicula
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los datos del videojuego: {str(e)}")