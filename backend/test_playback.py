"""
Test manual del PlaybackService.
Verifica que el control de reproduccion funciona correctamente,
incluyendo los eventos publicados en Redis.

Uso:
    cd backend
    python test_playback.py
"""
import asyncio
import json
import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient
from repositories.videogame_repo import VideogameRepository
from repositories.film_repo import FilmRepository
from services.playback_service import PlaybackService
from events.publisher import EventPublisher

MONGO_URI = "mongodb://localhost:27017"
REDIS_URL = "redis://localhost:6379"
DB_NAME   = "arcadiax_test"


async def main():
    # Conexiones
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    redis_client = redis.from_url(REDIS_URL)

    videogame_repo = VideogameRepository(db["videogames"])
    film_repo = FilmRepository(db["films"])
    publisher = EventPublisher(REDIS_URL)
    service = PlaybackService(videogame_repo, film_repo, publisher)

    # Suscribirse al canal Redis para capturar eventos
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("arcadiax")
    eventos_recibidos = []

    async def leer_eventos():
        async for msg in pubsub.listen():
            if msg["type"] == "message":
                eventos_recibidos.append(json.loads(msg["data"]))
                if len(eventos_recibidos) >= 3:  # Esperamos 3 eventos en total
                    break

    print("\n=== TEST PlaybackService ===\n")

    # Insertar datos de prueba
    crash_id = (await videogame_repo.create({
        "nombre": "Crash", "consola": "ps1",
        "ubicacion": "/roms/crash.bin", "play": False, "abierto": False
    }))["_id"]
    inception_id = (await film_repo.create({
        "nombre": "Inception", "ubicacion": "/films/inception.mkv",
        "play": False, "abierto": False
    }))["_id"]

    # 1. CURRENT sin nada reproduciendose
    print("--- GET CURRENT (vacio) ---")
    current = await service.get_current()
    assert current["type"] == "none", f"Esperaba 'none', got {current['type']}"
    print(f"OK: {current}")

    # Iniciar escucha de eventos en background
    task = asyncio.create_task(leer_eventos())

    # 2. PLAY GAME
    print("\n--- PLAY GAME ---")
    game = await service.play_game("Crash", "ps1")
    assert game["play"] == True
    print(f"OK: {game['nombre']} play={game['play']}")

    # 3. CURRENT con juego reproduciendose
    print("\n--- GET CURRENT (juego) ---")
    current = await service.get_current()
    assert current["type"] == "game"
    assert current["data"]["nombre"] == "Crash"
    print(f"OK: type={current['type']}, nombre={current['data']['nombre']}")

    # 4. Intentar poner otra cosa mientras hay juego (debe fallar)
    print("\n--- PLAY FILM mientras hay juego (debe dar 400) ---")
    try:
        await service.play_film("Inception")
        print("ERROR: debia haber lanzado excepcion")
    except Exception as e:
        print(f"OK: {e}")

    # 5. STOP
    print("\n--- STOP ---")
    await service.stop_playback()
    current = await service.get_current()
    assert current["type"] == "none"
    print("OK: playback detenido")

    # 6. PLAY FILM
    print("\n--- PLAY FILM ---")
    film = await service.play_film("Inception")
    assert film["play"] == True
    print(f"OK: {film['nombre']} play={film['play']}")

    # Esperar a que se reciban los eventos
    await task

    # 7. Verificar eventos recibidos
    print("\n--- EVENTOS RECIBIDOS ---")
    for evento in eventos_recibidos:
        print(evento)
    
    assert len(eventos_recibidos) == 3, "Esperaba recibir 3 eventos"
    assert eventos_recibidos[0]["event"] == Events.GAME_PLAY
    assert eventos_recibidos[1]["event"] == Events.PLAYBACK_STOP
    assert eventos_recibidos[2]["event"] == Events.FILM_PLAY
    print("OK: eventos recibidos correctamente")

if __name__ == "__main__":
    asyncio.run(main())
