import redis.asyncio as redis
import json


class EventPublisher:
    """
    Publica eventos en Redis usando pub/sub.
    El canal es "arcadiax" — cualquier modulo suscrito recibe el mensaje al instante.
    """

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)

    async def publish(self, event: str, data: dict):
        """
        Publica un evento en el canal arcadiax.
        Formato: {"event": "playback.game.play", "data": {"nombre": "Crash", ...}}
        """
        message = json.dumps({"event": event, "data": data})
        await self.redis.publish("arcadiax", message)

    async def close(self):
        await self.redis.close()
