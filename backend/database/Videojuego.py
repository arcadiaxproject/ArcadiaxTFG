from motor.motor_asyncio import AsyncIOMotorClient
from routes.models.Videojuego import Videogame
from bson import ObjectId
from fastapi import HTTPException
client=AsyncIOMotorClient("mongodb+srv://javier:javier@cluster0.t5cgbal.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
database=client.arcadedatabe
collection=database.arcade

async def get_one_videogame_id(id):
    try:
        # Validar si el id es un ObjectId válido
        if not ObjectId.is_valid(id):
            raise ValueError("El id proporcionado no es un ObjectId válido")

        videogame = await collection.find_one({"_id": ObjectId(id)})
        return videogame
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def get_one_videogame_nombre_consola(nombre: str, consola: str):
    # Hacer la consulta a MongoDB
    videogame = await collection.find_one({"nombre": nombre, "consola": consola})
    return videogame


async def get_all_videogame():
    videogames=[]
    cursor= collection.find({})
    async for document in cursor:
        videogames.append(Videogame(**document))
    return videogames

async def create_videogame(videogame):
    new_videogame= await collection.insert_one(videogame)
    videojuego_created=await collection.find_one({"_id":new_videogame.inserted_id})
    return videojuego_created

async def update_videogame(id:str, data):
    # Filtrar los campos con valores no nulos
    videogame = {k: v for k, v in data.dict().items() if v is not None}
    print(videogame)
    await collection.update_one({"_id":ObjectId(id)},{"$set":videogame})
    document=await collection.find_one({"_id":ObjectId(id)})
    return document


async def delete_videogame(id:str):
    videogame= await collection.delete_one({"_id":ObjectId(id)})
    return True

async def obtener_consolas():
    try:
        # Método distinct para obtener consolas únicas
        consolas = await collection.distinct("consola")
        # Elimina 'psp' de la lista
        consolas_filtradas = [consola for consola in consolas if consola != "psp"]
        return consolas_filtradas
    except Exception as e:
        # Manejo de errores genéricos y envío de un código HTTP 500
        raise HTTPException(status_code=500, detail=f"Error al obtener consolas: {str(e)}")
async def obtener_consola_historia():
    try:
        # Busca si existe la consola PSP en la colección
        consola_psp = await collection.find_one({"consola": "psp"})  # Cambiado "nds" por "PSP"
        if consola_psp:
            return "psp"
        else:
            return {"mensaje": "La consola PSP no está registrada en la base de datos."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def obtener_juegos_por_consola(consola: str):
    try:
        # Filtra los videojuegos por la consola especificada
        juegos = await collection.find({"consola": consola}).to_list(length=None)
        return juegos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#modifica el play a true a traves del nombre y la consola
async def set_play_true(nombre: str, consola: str):
    # Buscamos el videojuego por nombre y consola
    filtro = {"nombre": nombre, "consola": consola}
    
    # Actualizamos el campo 'play' a true
    resultado = await collection.update_one(filtro, {"$set": {"play": True}})
    
    if resultado.matched_count > 0:
        # Obtenemos el documento actualizado
        document = await collection.find_one(filtro)
        return document
    else:
        return {"mensaje": "Videojuego no encontrado"}
    
async def existe_videogame_en_play():
    # Devuelve True si encuentra un videojuego con 'play' a True, de lo contrario False
    return await collection.find_one({"play": True}) is not None



#reproduciendo a false y play a false
async def resetear_videogames():
    # Actualiza todos los documentos estableciendo 'play' y 'reproduciendo' a False
    resultado = await collection.update_many(
        {},
        {"$set": {"play": False, "abierto": False}}
    )
    return resultado.modified_count


