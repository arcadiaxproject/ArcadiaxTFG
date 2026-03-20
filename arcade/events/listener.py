import redis.asyncio as redis
import json
import logging

log = logging.getLogger("arcadiax.events")


class EventListener:
    """
    Se suscribe al canal "arcadiax" de Redis y ejecuta handlers
    cuando llegan eventos.

    Uso:
        handlers = {
            Events.GAME_PLAY: mi_funcion_async,
            Events.PLAYBACK_STOP: otra_funcion_async,
        }
        listener = EventListener(handlers)
        await listener.listen()
    """

    def __init__(self, handlers: dict, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.handlers = handlers

    async def listen(self):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe("arcadiax")
        log.info("Escuchando eventos en canal 'arcadiax'")

        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            try:
                payload = json.loads(message["data"])
                event = payload["event"]
                data = payload["data"]
                handler = self.handlers.get(event)
                if handler:
                    await handler(data)
            except (json.JSONDecodeError, KeyError) as e:
                log.error(f"Error procesando evento: {e}")
