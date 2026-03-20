import redis.asyncio as redis
import json


class EventPublisher:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)

    async def publish(self, event: str, data: dict):
        message = json.dumps({"event": event, "data": data})
        await self.redis.publish("arcadiax", message)

    async def close(self):
        await self.redis.close()
