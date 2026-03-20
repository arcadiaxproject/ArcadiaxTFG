"""
Test manual del BaseRepository.
Prueba los 5 metodos CRUD contra MongoDB real.

Uso:
    cd backend
    python test_base_repo.py
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from repositories.base import BaseRepository


MONGO_URI = "mongodb://localhost:27017"
MONGO_DB  = "arcadiax_test"   # Base de datos de prueba, separada de la real


async def main():
    # Conexion a MongoDB
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB]
    repo = BaseRepository(db["test_items"])

    print("\n=== TEST BaseRepository ===\n")

    # 1. CREATE
    print("--- CREATE ---")
    item = await repo.create({"nombre": "Crash Bandicoot", "consola": "ps1"})
    print(f"Creado: {item}")
    item_id = item["_id"]

    # 2. FIND ALL
    print("\n--- FIND ALL ---")
    todos = await repo.find_all()
    print(f"Total documentos: {len(todos)}")
    print(f"Primero: {todos[0]}")

    # 3. FIND BY ID
    print("\n--- FIND BY ID ---")
    encontrado = await repo.find_by_id(item_id)
    print(f"Encontrado por ID: {encontrado}")

    # 4. FIND BY ID (no existe)
    print("\n--- FIND BY ID (ID inexistente) ---")
    no_existe = await repo.find_by_id("000000000000000000000000")
    print(f"Resultado (debe ser None): {no_existe}")

    # 5. UPDATE
    print("\n--- UPDATE ---")
    actualizado = await repo.update(item_id, {"nombre": "Crash Bandicoot 2"})
    print(f"Actualizado: {actualizado}")

    # 6. UPDATE con todos None (no debe cambiar nada)
    print("\n--- UPDATE sin cambios (todos None) ---")
    sin_cambio = await repo.update(item_id, {"nombre": None, "consola": None})
    print(f"Sin cambio: {sin_cambio}")

    # 7. FIND ALL con filtro
    print("\n--- FIND ALL con filtro ---")
    await repo.create({"nombre": "Spyro", "consola": "ps1"})
    await repo.create({"nombre": "Mario 64", "consola": "n64"})
    ps1_games = await repo.find_all({"consola": "ps1"})
    print(f"Juegos de ps1 (deben ser 2): {len(ps1_games)}")

    # 8. DELETE
    print("\n--- DELETE ---")
    eliminado = await repo.delete(item_id)
    print(f"Eliminado (debe ser True): {eliminado}")
    tras_borrar = await repo.find_by_id(item_id)
    print(f"Tras borrar (debe ser None): {tras_borrar}")

    # 9. DELETE inexistente
    print("\n--- DELETE inexistente ---")
    no_eliminado = await repo.delete("000000000000000000000000")
    print(f"No eliminado (debe ser False): {no_eliminado}")

    # Limpieza: borrar la coleccion de prueba
    await db["test_items"].drop()
    client.close()

    print("\n=== TODOS LOS TESTS PASADOS ===\n")


asyncio.run(main())
