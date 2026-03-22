from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes import videogames, films, playback
from events.publisher import EventPublisher
from shared.events import Events
import redis

app = FastAPI(title="ArcadiaX API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videogames.router)
app.include_router(films.router)
app.include_router(playback.router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "arcadiax-backend"}


# WebSocket endpoint to emit Redis events
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()
redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
pubsub = redis_client.pubsub()
pubsub.subscribe(Events.REDIS_CHANNEL)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            message = pubsub.get_message(timeout=None)
            if message and isinstance(message, dict) and message['type'] == 'message':
                await manager.broadcast(message['data'].decode('utf-8'))
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.BACKEND_HOST, port=settings.BACKEND_PORT, reload=True)
