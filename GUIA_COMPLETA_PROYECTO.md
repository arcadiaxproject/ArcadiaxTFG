# ArcadiaX v2 — Guía completa del proyecto (código comentado línea a línea)

> Este documento explica TODO el código del proyecto ArcadiaX v2 desde cero.
> Cada archivo está incluido con su código completo y explicaciones detalladas.
> Pensado para seguirlo mientras se graba el vídeo o para consulta.

---

# PARTE 1: CONFIGURACIÓN BASE

---

## 1.1 Variables de entorno — `.env`

Las variables de entorno permiten configurar el sistema sin tocar código. Cada módulo lee lo que necesita de aquí.

```bash
# MongoDB — base de datos donde se guardan juegos y películas
MONGO_URI=mongodb://localhost:27017    # Dirección del servidor MongoDB
MONGO_DB=arcadiax                      # Nombre de la base de datos

# Redis — sistema de mensajería entre módulos
REDIS_URL=redis://localhost:6379       # Dirección del servidor Redis

# Backend — API REST
BACKEND_HOST=0.0.0.0                   # Escucha en todas las interfaces de red
BACKEND_PORT=8000                      # Puerto del backend

# Frontend — Interfaz web React
REACT_APP_API_URL=http://localhost:8000 # URL donde el frontend busca el backend

# Arcade — Rutas a emuladores y contenido
RETROARCH_PATH=/Applications/RetroArch.app/Contents/MacOS/RetroArch
PPSSPP_PATH=/Applications/PPSSPP.app/Contents/MacOS/PPSSPP
ROMS_PATH=~/roms                       # Carpeta donde están las ROMs
TRAILERS_PATH=~/trailers               # Carpeta donde están los vídeos de trailers
MEDIA_PLAYER=mpv                       # Reproductor para trailers (mpv o vlc)
```

**Por qué `.env`:** Si mañana cambias de puerto o de ruta de emuladores, lo cambias aquí sin tocar ni una línea de código.

---

## 1.2 `.gitignore`

Archivos que Git debe ignorar para no subir basura al repositorio:

```
.env                 # Contiene configuración local, no debe subirse
__pycache__/         # Cache de Python compilado
*.pyc                # Archivos Python compilados
node_modules/        # Dependencias de npm (se regeneran con npm install)
build/               # Build de producción del frontend
dist/                # Distribuciones
.venv/               # Entorno virtual de Python
venv/
*.egg-info/          # Metadata de paquetes Python
.pytest_cache/       # Cache de tests
```

---

## 1.3 Docker Compose — `docker-compose.yml`

Docker Compose permite levantar todos los servicios con un solo comando: `docker compose up -d`.

```yaml
services:
  # Base de datos MongoDB
  # Almacena videojuegos, películas y su estado
  mongodb:
    image: mongo:7                    # Imagen oficial de MongoDB versión 7
    ports:
      - "27017:27017"                 # Expone el puerto estándar de MongoDB
    volumes:
      - mongo_data:/data/db           # Los datos persisten aunque se pare el contenedor

  # Redis — Sistema de mensajería pub/sub
  # Permite que el backend y el arcade se comuniquen por eventos
  redis:
    image: redis:7-alpine             # Versión ligera de Redis (~5MB)
    ports:
      - "6379:6379"                   # Puerto estándar de Redis

  # Backend — API REST con FastAPI
  backend:
    build: ./backend                  # Construye desde el Dockerfile del backend
    ports:
      - "8000:8000"                   # Puerto de la API
    env_file: .env                    # Carga las variables de entorno
    depends_on:                       # Espera a que estos servicios arranquen primero
      - mongodb
      - redis

  # Frontend — Interfaz web con React
  frontend:
    build: ./frontend                 # Construye desde el Dockerfile del frontend
    ports:
      - "3000:3000"                   # Puerto del frontend
    depends_on:
      - backend                       # Necesita el backend para las llamadas API

# Volúmenes persistentes — los datos de MongoDB sobreviven a reinicios
volumes:
  mongo_data:
```

**Uso:**
```bash
docker compose up -d          # Levanta todo en segundo plano
docker compose logs -f        # Ver logs en tiempo real
docker compose down           # Para todo
docker compose up mongodb redis -d  # Solo levantar BBDD y Redis (para desarrollo)
```

---

# PARTE 2: SHARED — Código compartido entre módulos

---

## 2.1 Definición de eventos — `shared/events.py`

Este archivo define TODOS los eventos del sistema como constantes. Así no hay strings mágicos sueltos por el código. Si cambias el nombre de un evento, lo cambias aquí y listo.

```python
class Events:
    # ── INPUT ──────────────────────────────────────────
    # Eventos que se disparan cuando el usuario interactúa

    ARCADE_BUTTON_SELECT = "input.arcade.select"
    # Se publica cuando alguien pulsa el botón de selección en la máquina arcade física.
    # El arcade engine lo recibe y cambia al estado SELECTING.

    ARCADE_BUTTON_BACK = "input.arcade.back"
    # Se publica cuando se pulsa el botón de "atrás" en el arcade.
    # Si estás en selección → vuelve a IDLE.
    # Si estás jugando → cierra el emulador.

    ARCADE_BUTTON_CONFIRM = "input.arcade.confirm"
    # Se publica cuando se pulsa el botón de confirmar.
    # En pantalla de selección, confirma el juego elegido.

    WEB_SELECT_REQUEST = "input.web.select"
    # Se publica cuando alguien abre la app web (desde el móvil o PC).
    # Tiene el mismo efecto que ARCADE_BUTTON_SELECT.
    # Esto permite que ambas entradas (física y web) usen el mismo flujo.

    # ── ESTADO ─────────────────────────────────────────

    STATE_CHANGED = "state.changed"
    # Se publica cada vez que la máquina de estados cambia.
    # El frontend lo puede escuchar para actualizar la interfaz en tiempo real.
    # Payload: {"state": "idle|trailer|selecting|loading|playing|saving"}

    # ── PLAYBACK ───────────────────────────────────────
    # Eventos relacionados con la reproducción de contenido

    GAME_PLAY = "playback.game.play"
    # Se publica cuando un usuario elige un juego (desde la web o el arcade).
    # Payload: {"nombre": "Crash", "consola": "ps1", "ubicacion": "/roms/crash.bin"}
    # El arcade engine lo recibe, busca el driver correcto y lanza el emulador.

    GAME_OPENED = "playback.game.opened"
    # Se publica cuando el emulador ha arrancado correctamente.

    GAME_CLOSED = "playback.game.closed"
    # Se publica cuando el emulador se ha cerrado (el usuario dejó de jugar).

    FILM_PLAY = "playback.film.play"
    # Se publica cuando un usuario elige una película.
    # Payload: {"nombre": "Inception", "ubicacion": "/peliculas/inception.mkv"}

    PLAYBACK_STOP = "playback.stop"
    # Se publica cuando se para toda la reproducción.
    # Resetea el estado de juegos y películas en la BBDD.

    # ── SISTEMA ────────────────────────────────────────

    IDLE_DETECTED = "system.idle"
    # Se publica cuando el sistema lleva X segundos sin actividad.

    SYSTEM_SHUTDOWN = "system.shutdown"
    # Se publica cuando se va a apagar el sistema.
```

**Convención de nombres:** `categoria.subcategoria.accion`. Así puedes filtrar por categoría si lo necesitas en el futuro.

---

## 2.2 Logger unificado — `shared/logger.py`

Logger configurable que todos los módulos usan para imprimir mensajes con el mismo formato.

```python
import logging
import sys


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Crea un logger con formato unificado para todo el proyecto.

    Uso:
        from shared.logger import setup_logger
        log = setup_logger("arcadiax.backend")
        log.info("Servidor arrancado")
        # Output: [14:32:05] arcadiax.backend | INFO | Servidor arrancado

    Args:
        name: Nombre del logger (normalmente "arcadiax.modulo")
        level: Nivel mínimo de log (DEBUG, INFO, WARNING, ERROR)
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evitar duplicar handlers si se llama varias veces
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)  # Imprime en la terminal
        handler.setLevel(level)

        # Formato: [HH:MM:SS] nombre | NIVEL | mensaje
        formatter = logging.Formatter(
            "[%(asctime)s] %(name)s | %(levelname)s | %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
```

**Por qué un logger custom:** En vez de usar `print()` por todos lados (como en la v1), todos los módulos usan el mismo formato con timestamp, nivel y módulo. Esto hace que los logs sean fáciles de leer y filtrar.

---

# PARTE 3: BACKEND — API REST con FastAPI

El backend es una API REST que gestiona videojuegos y películas. Está organizado en 3 capas:

```
Petición HTTP → Ruta (recibe y valida) → Service (lógica) → Repository (BBDD)
```

Cada capa tiene una única responsabilidad. Si necesitas cambiar cómo se accede a la BBDD, solo tocas el repository. Si necesitas cambiar una regla de negocio, solo tocas el service. Las rutas nunca cambian por dentro.

---

## 3.1 Configuración — `backend/config.py`

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Lee las variables de entorno y las convierte en un objeto Python tipado.

    pydantic-settings hace lo siguiente automáticamente:
    1. Busca el archivo .env en la raíz del proyecto
    2. Lee las variables que coinciden con los nombres de los atributos
    3. Las convierte al tipo correcto (str, int, etc.)
    4. Si no encuentra una variable, usa el valor por defecto

    Ejemplo: si en .env pones BACKEND_PORT=9000, settings.BACKEND_PORT será 9000 (int).
    Si no pones nada, será 8000 por defecto.
    """
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "arcadiax"
    REDIS_URL: str = "redis://localhost:6379"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    class Config:
        env_file = ".env"    # Busca el archivo .env en el directorio actual


# Instancia global — se importa desde cualquier archivo del backend
settings = Settings()
```

---

## 3.2 Conexión a MongoDB — `backend/database.py`

```python
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

# Motor es el driver asíncrono de MongoDB para Python.
# A diferencia de PyMongo (síncrono), Motor no bloquea el servidor
# mientras espera respuestas de la base de datos.
# Esto es importante porque FastAPI es asíncrono (async/await).

client = AsyncIOMotorClient(settings.MONGO_URI)
# Crea una conexión al servidor MongoDB.
# No se conecta realmente hasta que hagas una operación (lazy connection).

db = client[settings.MONGO_DB]
# Selecciona la base de datos "arcadiax".
# Si no existe, MongoDB la crea automáticamente cuando insertes el primer documento.
# Dentro de db tendremos colecciones: db["videogames"], db["films"], etc.
```

---

## 3.3 Modelos Pydantic — `backend/models/`

Los modelos Pydantic validan los datos que entran y salen de la API. Si alguien envía un campo con el tipo incorrecto, Pydantic devuelve un error 422 automáticamente.

### `backend/models/videogame.py`

```python
from pydantic import BaseModel, Field
from typing import Optional


class VideogameCreate(BaseModel):
    """
    Modelo para CREAR un videojuego (POST).
    Define los campos obligatorios y opcionales que el usuario debe enviar.

    Ejemplo de JSON que acepta:
    {
        "nombre": "Crash Bandicoot",
        "consola": "ps1",
        "ubicacion": "/roms/ps1/crash.bin",
        "trailer": "/trailers/crash.mp4",
        "imagen": "crash.jpg"
    }
    """
    nombre: str                # Obligatorio — nombre del juego
    consola: str               # Obligatorio — a qué consola pertenece
    ubicacion: str = ""        # Opcional — ruta al archivo ROM
    trailer: str = ""          # Opcional — ruta al vídeo del trailer
    imagen: str = ""           # Opcional — nombre del archivo de imagen


class VideogameUpdate(BaseModel):
    """
    Modelo para ACTUALIZAR un videojuego (PUT).
    Todos los campos son opcionales — solo se actualizan los que envíes.

    Ejemplo: si solo quieres cambiar la imagen:
    {"imagen": "crash_nuevo.jpg"}
    """
    nombre: Optional[str] = None
    consola: Optional[str] = None
    ubicacion: Optional[str] = None
    trailer: Optional[str] = None
    imagen: Optional[str] = None


class VideogameResponse(BaseModel):
    """
    Modelo de RESPUESTA — lo que la API devuelve al cliente.
    Incluye los campos internos como id, play y abierto.

    Field(alias="_id"):
    MongoDB guarda el id como "_id". Este alias le dice a Pydantic
    que cuando reciba "_id" del documento de MongoDB, lo mapee al campo "id".

    populate_by_name = True:
    Permite que el modelo acepte tanto "id" como "_id" como nombre del campo.
    """
    id: str = Field(alias="_id")
    nombre: str
    consola: str
    ubicacion: str = ""
    trailer: str = ""
    imagen: str = ""
    play: bool = False         # ¿Está reproduciéndose ahora?
    abierto: bool = False      # ¿El emulador ya lo ha abierto?

    class Config:
        populate_by_name = True
```

### `backend/models/film.py`

```python
from pydantic import BaseModel, Field
from typing import Optional


class FilmCreate(BaseModel):
    """
    Modelo para crear una película.
    Mismo patrón que VideogameCreate pero sin campo "consola".
    """
    nombre: str
    ubicacion: str = ""        # Ruta al archivo de vídeo
    trailer: str = ""          # Ruta al trailer
    imagen: str = ""           # Nombre del archivo de imagen


class FilmUpdate(BaseModel):
    """Modelo para actualizar — todos los campos opcionales."""
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    trailer: Optional[str] = None
    imagen: Optional[str] = None


class FilmResponse(BaseModel):
    """Modelo de respuesta con id y estado de reproducción."""
    id: str = Field(alias="_id")
    nombre: str
    ubicacion: str = ""
    trailer: str = ""
    imagen: str = ""
    play: bool = False
    abierto: bool = False

    class Config:
        populate_by_name = True
```

---

## 3.4 Repositories — Acceso a datos (`backend/repositories/`)

Los repositories son la ÚNICA capa que habla con MongoDB. Nadie más en el proyecto hace queries directamente a la base de datos.

### `backend/repositories/base.py` — CRUD genérico

```python
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import Optional


class BaseRepository:
    """
    Repositorio base con operaciones CRUD genéricas.

    Cualquier entidad nueva (música, series, usuarios...) hereda de aquí
    y automáticamente tiene find_all, find_by_id, create, update y delete.

    Uso:
        repo = BaseRepository(db["videogames"])
        games = await repo.find_all()
        game = await repo.find_by_id("507f1f77bcf86cd799439011")
    """

    def __init__(self, collection: AsyncIOMotorCollection):
        """
        Recibe la colección de MongoDB sobre la que operar.
        Ejemplo: BaseRepository(db["videogames"]) opera sobre la colección "videogames".
        """
        self.collection = collection

    async def find_all(self, filtro: dict = None) -> list:
        """
        Devuelve todos los documentos de la colección.

        Args:
            filtro: Filtro MongoDB opcional. Ejemplo: {"consola": "ps1"}
                    Si no se pasa filtro, devuelve todos.

        El cursor.to_list(length=500) convierte el cursor de MongoDB en una lista Python.
        Limitamos a 500 para evitar cargar toda la BBDD en memoria.

        El bucle convierte _id de ObjectId a string porque JSON no sabe
        serializar ObjectId (es un tipo propio de MongoDB).
        """
        cursor = self.collection.find(filtro or {})
        docs = await cursor.to_list(length=500)
        for doc in docs:
            doc["_id"] = str(doc["_id"])  # ObjectId → string
        return docs

    async def find_by_id(self, id: str) -> Optional[dict]:
        """
        Busca un documento por su ID.

        ObjectId(id) convierte el string "507f1f77..." en un ObjectId de MongoDB,
        que es el tipo que MongoDB usa internamente para los _id.

        Devuelve None si no lo encuentra (no lanza excepción).
        """
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def create(self, data: dict) -> dict:
        """
        Inserta un documento nuevo en la colección.

        insert_one devuelve un objeto con inserted_id (el ID que MongoDB generó).
        Añadimos ese ID al diccionario original para devolverlo completo.
        """
        result = await self.collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data

    async def update(self, id: str, data: dict) -> Optional[dict]:
        """
        Actualiza un documento existente.

        Primero filtra los campos None para no sobreescribir datos existentes
        con valores vacíos. Si envías {"nombre": "Crash", "consola": None},
        solo actualiza "nombre".

        find_one_and_update con return_document=True devuelve el documento
        DESPUÉS de actualizarlo (no el original).

        $set es el operador de MongoDB para actualizar campos específicos
        sin borrar el resto del documento.
        """
        update_data = {k: v for k, v in data.items() if v is not None}
        if not update_data:
            return await self.find_by_id(id)
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(id)},             # Filtro: busca por ID
            {"$set": update_data},             # Operación: actualiza estos campos
            return_document=True               # Devuelve el documento actualizado
        )
        if result:
            result["_id"] = str(result["_id"])
        return result

    async def delete(self, id: str) -> bool:
        """
        Elimina un documento por su ID.
        Devuelve True si se eliminó, False si no existía.
        """
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
```

### `backend/repositories/videogame_repo.py` — Queries específicas de videojuegos

```python
from repositories.base import BaseRepository
from typing import Optional


class VideogameRepository(BaseRepository):
    """
    Repositorio de videojuegos. Hereda todo el CRUD del BaseRepository
    y añade queries específicas que solo tienen sentido para videojuegos.
    """

    async def find_by_name_and_console(self, nombre: str, consola: str) -> Optional[dict]:
        """
        Busca un juego por nombre + consola.
        Se usa para verificar si ya existe antes de crear uno nuevo.
        La combinación nombre+consola es única (no puedes tener dos "Crash" en "ps1").
        """
        doc = await self.collection.find_one({"nombre": nombre, "consola": consola})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def get_consoles(self) -> list[str]:
        """
        Devuelve una lista de consolas únicas.
        distinct("consola") es como un SELECT DISTINCT en SQL.
        Si tienes juegos de ps1, snes y gba, devuelve ["ps1", "snes", "gba"].
        """
        return await self.collection.distinct("consola")

    async def get_by_console(self, consola: str) -> list:
        """
        Devuelve todos los juegos de una consola específica.
        Usa find_all del BaseRepository pasándole un filtro.
        """
        return await self.find_all({"consola": consola})

    async def get_playing(self) -> Optional[dict]:
        """
        Devuelve el juego que se está reproduciendo ahora (play=True).
        Solo puede haber uno a la vez (el service se encarga de eso).
        """
        doc = await self.collection.find_one({"play": True})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def is_any_playing(self) -> bool:
        """
        Comprueba si hay algún juego reproduciéndose.
        Más eficiente que get_playing() porque no devuelve el documento completo.
        """
        doc = await self.collection.find_one({"play": True})
        return doc is not None

    async def set_play(self, nombre: str, consola: str) -> Optional[dict]:
        """
        Marca un juego como "en reproducción" (play=True).
        Busca por nombre+consola y actualiza el campo play.
        """
        result = await self.collection.find_one_and_update(
            {"nombre": nombre, "consola": consola},
            {"$set": {"play": True}},
            return_document=True
        )
        if result:
            result["_id"] = str(result["_id"])
        return result

    async def set_opened(self, nombre: str, consola: str) -> Optional[dict]:
        """
        Marca un juego como "abierto" (el emulador ya lo cargó).
        Diferencia entre play y abierto:
        - play=True: el usuario quiere jugar esto
        - abierto=True: el emulador ya se ha abierto con este juego
        """
        result = await self.collection.find_one_and_update(
            {"nombre": nombre, "consola": consola},
            {"$set": {"abierto": True}},
            return_document=True
        )
        if result:
            result["_id"] = str(result["_id"])
        return result

    async def reset_all(self) -> int:
        """
        Resetea TODOS los juegos: play=False, abierto=False.
        Se llama cuando se para la reproducción.
        update_many actualiza todos los documentos que coincidan (en este caso, todos).
        Devuelve cuántos documentos se modificaron.
        """
        result = await self.collection.update_many(
            {},                                            # Sin filtro = todos
            {"$set": {"play": False, "abierto": False}}
        )
        return result.modified_count

    async def get_random_trailer(self) -> Optional[str]:
        """
        Devuelve la URL/ruta de un trailer aleatorio.

        Pipeline de agregación MongoDB:
        1. $match: filtra juegos que tengan trailer (no vacío)
        2. $sample: elige 1 al azar

        Esto es más eficiente que traer todos y elegir uno con random.choice().
        """
        pipeline = [
            {"$match": {"trailer": {"$exists": True, "$ne": ""}}},
            {"$sample": {"size": 1}}
        ]
        results = await self.collection.aggregate(pipeline).to_list(length=1)
        return results[0]["trailer"] if results else None
```

### `backend/repositories/film_repo.py` — Queries específicas de películas

```python
from repositories.base import BaseRepository
from typing import Optional


class FilmRepository(BaseRepository):
    """
    Repositorio de películas. Mismo patrón que VideogameRepository
    pero adaptado: las películas se buscan solo por nombre (no tienen consola).
    """

    async def find_by_name(self, nombre: str) -> Optional[dict]:
        """Busca una película por nombre. Se usa para evitar duplicados."""
        doc = await self.collection.find_one({"nombre": nombre})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def get_playing(self) -> Optional[dict]:
        """Devuelve la película que se está reproduciendo (play=True)."""
        doc = await self.collection.find_one({"play": True})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def is_any_playing(self) -> bool:
        """Comprueba si hay alguna película reproduciéndose."""
        doc = await self.collection.find_one({"play": True})
        return doc is not None

    async def set_play(self, nombre: str) -> Optional[dict]:
        """Marca una película como en reproducción."""
        result = await self.collection.find_one_and_update(
            {"nombre": nombre},
            {"$set": {"play": True}},
            return_document=True
        )
        if result:
            result["_id"] = str(result["_id"])
        return result

    async def set_opened(self, nombre: str) -> Optional[dict]:
        """Marca una película como abierta (el reproductor la cargó)."""
        result = await self.collection.find_one_and_update(
            {"nombre": nombre},
            {"$set": {"abierto": True}},
            return_document=True
        )
        if result:
            result["_id"] = str(result["_id"])
        return result

    async def reset_all(self) -> int:
        """Resetea todas las películas."""
        result = await self.collection.update_many(
            {},
            {"$set": {"play": False, "abierto": False}}
        )
        return result.modified_count

    async def get_random_trailer(self) -> Optional[str]:
        """Devuelve un trailer aleatorio de películas."""
        pipeline = [
            {"$match": {"trailer": {"$exists": True, "$ne": ""}}},
            {"$sample": {"size": 1}}
        ]
        results = await self.collection.aggregate(pipeline).to_list(length=1)
        return results[0]["trailer"] if results else None
```

---

## 3.5 Services — Lógica de negocio (`backend/services/`)

Los services contienen las reglas del sistema. "¿Se puede jugar ahora?" "¿Ya existe este juego?" Las decisiones se toman aquí, no en las rutas ni en los repositories.

### `backend/services/videogame_service.py`

```python
from repositories.videogame_repo import VideogameRepository
from fastapi import HTTPException


class VideogameService:
    """
    Lógica de negocio para videojuegos.
    Recibe un repository en el constructor (inyección de dependencias).
    Así si mañana cambias de MongoDB a PostgreSQL, solo cambias el repository.
    """

    def __init__(self, repo: VideogameRepository):
        self.repo = repo

    async def get_all(self) -> list:
        """Devuelve todos los videojuegos. Sin lógica adicional."""
        return await self.repo.find_all()

    async def get_by_id(self, id: str) -> dict:
        """
        Busca un juego por ID.
        Si no existe, lanza HTTPException 404.
        El service decide qué es un error, no el repository.
        """
        game = await self.repo.find_by_id(id)
        if not game:
            raise HTTPException(404, f"Videojuego no encontrado: {id}")
        return game

    async def get_consoles(self) -> list[str]:
        """Devuelve la lista de consolas únicas."""
        consoles = await self.repo.get_consoles()
        if not consoles:
            raise HTTPException(404, "No se encontraron consolas")
        return consoles

    async def get_by_console(self, consola: str) -> list:
        """Devuelve todos los juegos de una consola."""
        games = await self.repo.get_by_console(consola)
        if not games:
            raise HTTPException(404, f"No hay juegos para: {consola}")
        return games

    async def create(self, data: dict) -> dict:
        """
        Crea un videojuego nuevo.

        Regla de negocio: no puede haber dos juegos con el mismo nombre+consola.
        Si ya existe "Crash Bandicoot" en "ps1", devuelve error 409 (Conflict).

        Antes de guardar, inicializa play=False y abierto=False.
        """
        existing = await self.repo.find_by_name_and_console(
            data["nombre"], data["consola"]
        )
        if existing:
            raise HTTPException(409, "El videojuego ya existe")
        data["play"] = False
        data["abierto"] = False
        return await self.repo.create(data)

    async def update(self, id: str, data: dict) -> dict:
        """Actualiza un videojuego. Error 404 si no existe."""
        game = await self.repo.update(id, data)
        if not game:
            raise HTTPException(404, f"Videojuego no encontrado: {id}")
        return game

    async def delete(self, id: str) -> bool:
        """Elimina un videojuego. Error 404 si no existe."""
        deleted = await self.repo.delete(id)
        if not deleted:
            raise HTTPException(404, f"Videojuego no encontrado: {id}")
        return True
```

### `backend/services/film_service.py`

```python
from repositories.film_repo import FilmRepository
from fastapi import HTTPException


class FilmService:
    """Lógica de negocio para películas. Mismo patrón que VideogameService."""

    def __init__(self, repo: FilmRepository):
        self.repo = repo

    async def get_all(self) -> list:
        return await self.repo.find_all()

    async def get_by_name(self, nombre: str) -> dict:
        film = await self.repo.find_by_name(nombre)
        if not film:
            raise HTTPException(404, f"Película no encontrada: {nombre}")
        return film

    async def create(self, data: dict) -> dict:
        """
        Crea una película. Regla: no puede haber dos con el mismo nombre.
        """
        existing = await self.repo.find_by_name(data["nombre"])
        if existing:
            raise HTTPException(409, "La película ya existe")
        data["play"] = False
        data["abierto"] = False
        return await self.repo.create(data)

    async def delete(self, id: str) -> bool:
        deleted = await self.repo.delete(id)
        if not deleted:
            raise HTTPException(404, f"Película no encontrada: {id}")
        return True
```

### `backend/services/playback_service.py` — El service más importante

```python
from repositories.videogame_repo import VideogameRepository
from repositories.film_repo import FilmRepository
from events.publisher import EventPublisher
from shared.events import Events
from fastapi import HTTPException


class PlaybackService:
    """
    Controla QUÉ se está reproduciendo en el sistema.

    Este es el service más importante porque:
    1. Decide si se puede jugar/ver algo (¿hay algo ya reproduciéndose?)
    2. Publica eventos Redis para que el arcade engine actúe
    3. Coordina entre videojuegos y películas (no puedes jugar y ver peli a la vez)
    """

    def __init__(self, videogame_repo: VideogameRepository,
                 film_repo: FilmRepository, events: EventPublisher):
        self.videogames = videogame_repo
        self.films = film_repo
        self.events = events

    async def play_game(self, nombre: str, consola: str) -> dict:
        """
        Inicia la reproducción de un juego.

        Flujo:
        1. ¿Hay un juego ya reproduciéndose? → Error 400
        2. ¿Hay una película reproduciéndose? → Error 400
        3. Marca el juego como play=True en la BBDD
        4. Publica evento GAME_PLAY en Redis
        5. El arcade engine recibe el evento y abre el emulador
        """
        if await self.videogames.is_any_playing():
            raise HTTPException(400, "Ya hay un juego en reproducción")
        if await self.films.is_any_playing():
            raise HTTPException(400, "Hay una película en reproducción")

        game = await self.videogames.set_play(nombre, consola)
        if not game:
            raise HTTPException(404, f"Juego '{nombre}' ({consola}) no encontrado")

        # Publicar evento → el arcade engine lo recibe y abre el emulador
        await self.events.publish(Events.GAME_PLAY, {
            "nombre": nombre,
            "consola": consola,
            "ubicacion": game.get("ubicacion", "")
        })
        return game

    async def play_film(self, nombre: str) -> dict:
        """
        Inicia la reproducción de una película.
        Misma lógica que play_game pero para películas.
        """
        if await self.videogames.is_any_playing():
            raise HTTPException(400, "Hay un juego en reproducción")
        if await self.films.is_any_playing():
            raise HTTPException(400, "Ya hay una película en reproducción")

        film = await self.films.set_play(nombre)
        if not film:
            raise HTTPException(404, f"Película '{nombre}' no encontrada")

        await self.events.publish(Events.FILM_PLAY, {
            "nombre": nombre,
            "ubicacion": film.get("ubicacion", "")
        })
        return film

    async def stop(self):
        """
        Para toda la reproducción.
        Resetea todos los juegos y películas (play=False, abierto=False).
        Publica evento PLAYBACK_STOP para que el arcade cierre el emulador.
        """
        await self.videogames.reset_all()
        await self.films.reset_all()
        await self.events.publish(Events.PLAYBACK_STOP, {})

    async def get_current(self) -> dict:
        """
        Devuelve qué se está reproduciendo ahora.

        Respuestas posibles:
        {"type": "game", "data": {...}}   → hay un juego en marcha
        {"type": "film", "data": {...}}   → hay una película en marcha
        {"type": "none", "data": null}    → no hay nada reproduciéndose
        """
        game = await self.videogames.get_playing()
        if game:
            return {"type": "game", "data": game}
        film = await self.films.get_playing()
        if film:
            return {"type": "film", "data": film}
        return {"type": "none", "data": None}

    async def get_random_trailer(self) -> str:
        """
        Devuelve un trailer aleatorio (de juegos o pelis).
        Primero busca en juegos, si no hay, busca en películas.
        """
        trailer = await self.videogames.get_random_trailer()
        if not trailer:
            trailer = await self.films.get_random_trailer()
        if not trailer:
            raise HTTPException(404, "No hay trailers disponibles")
        return trailer
```

---

## 3.6 Publisher de eventos — `backend/events/publisher.py`

```python
import redis.asyncio as redis
import json


class EventPublisher:
    """
    Publica eventos en Redis usando el patrón pub/sub.

    Pub/sub funciona así:
    - Hay un "canal" (como una emisora de radio): "arcadiax"
    - El publisher emite mensajes en ese canal
    - Cualquier módulo suscrito al canal recibe el mensaje al instante
    - No hay cola: si nadie está escuchando, el mensaje se pierde
      (no pasa nada, significa que el arcade engine no está corriendo)
    """

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        # Crea una conexión a Redis.
        # redis.asyncio es la versión asíncrona del cliente Redis.
        self.redis = redis.from_url(redis_url)

    async def publish(self, event: str, data: dict):
        """
        Publica un evento en el canal "arcadiax".

        El mensaje es un JSON con dos campos:
        - event: nombre del evento (ej: "playback.game.play")
        - data: datos del evento (ej: {"nombre": "Crash", "consola": "ps1"})

        Ejemplo:
            await publisher.publish(Events.GAME_PLAY, {"nombre": "Crash"})
            # Redis recibe: {"event": "playback.game.play", "data": {"nombre": "Crash"}}
        """
        message = json.dumps({"event": event, "data": data})
        await self.redis.publish("arcadiax", message)

    async def close(self):
        """Cierra la conexión a Redis."""
        await self.redis.close()
```

---

## 3.7 Rutas — Endpoints HTTP (`backend/routes/`)

Las rutas son la capa más superficial. Solo hacen tres cosas:
1. Reciben la petición HTTP
2. La delegan al service
3. Devuelven la respuesta

No hay lógica de negocio ni acceso a datos aquí.

### `backend/routes/videogames.py`

```python
from fastapi import APIRouter, Depends
from models.videogame import VideogameCreate, VideogameUpdate, VideogameResponse
from services.videogame_service import VideogameService
from dependencies import get_videogame_service

# APIRouter agrupa endpoints bajo un prefijo común.
# Todos los endpoints de este archivo empiezan por /videogames
# tags=["videogames"] los agrupa en Swagger (la documentación automática)
router = APIRouter(prefix="/videogames", tags=["videogames"])


@router.get("/", response_model=list[VideogameResponse])
async def get_all(service: VideogameService = Depends(get_videogame_service)):
    """
    GET /videogames — Devuelve todos los videojuegos.

    Depends(get_videogame_service):
    FastAPI inyecta automáticamente una instancia de VideogameService.
    Esto se llama "inyección de dependencias" — la ruta no crea el service,
    lo recibe ya hecho. Así es fácil de testear (puedes inyectar un mock).

    response_model=list[VideogameResponse]:
    Le dice a FastAPI que la respuesta debe ser una lista de VideogameResponse.
    FastAPI valida que la respuesta cumpla el modelo y genera la doc de Swagger.
    """
    return await service.get_all()


@router.get("/consoles", response_model=list[str])
async def get_consoles(service: VideogameService = Depends(get_videogame_service)):
    """GET /videogames/consoles — Lista de consolas únicas."""
    return await service.get_consoles()


@router.get("/console/{consola}", response_model=list[VideogameResponse])
async def get_by_console(consola: str, service: VideogameService = Depends(get_videogame_service)):
    """
    GET /videogames/console/ps1 — Juegos de una consola.
    {consola} es un path parameter — FastAPI lo extrae de la URL automáticamente.
    """
    return await service.get_by_console(consola)


@router.get("/{id}", response_model=VideogameResponse)
async def get_by_id(id: str, service: VideogameService = Depends(get_videogame_service)):
    """GET /videogames/507f1f77bcf86cd799439011 — Un juego por ID."""
    return await service.get_by_id(id)


@router.post("/", response_model=VideogameResponse, status_code=201)
async def create(game: VideogameCreate, service: VideogameService = Depends(get_videogame_service)):
    """
    POST /videogames — Crear un juego nuevo.

    game: VideogameCreate — FastAPI lee el body JSON de la petición y lo convierte
    en un objeto VideogameCreate. Si falta un campo obligatorio o el tipo es
    incorrecto, devuelve 422 automáticamente.

    model_dump() convierte el objeto Pydantic a diccionario Python.

    status_code=201: devuelve 201 Created en vez del 200 por defecto.
    """
    return await service.create(game.model_dump())


@router.put("/{id}", response_model=VideogameResponse)
async def update(id: str, game: VideogameUpdate, service: VideogameService = Depends(get_videogame_service)):
    """
    PUT /videogames/{id} — Actualizar un juego.

    exclude_none=True: al convertir a dict, omite los campos que son None.
    Así si solo envías {"nombre": "Crash 2"}, no sobreescribe los demás campos.
    """
    return await service.update(id, game.model_dump(exclude_none=True))


@router.delete("/{id}")
async def delete(id: str, service: VideogameService = Depends(get_videogame_service)):
    """DELETE /videogames/{id} — Eliminar un juego."""
    await service.delete(id)
    return {"detail": "Videojuego eliminado"}
```

### `backend/routes/films.py`

```python
from fastapi import APIRouter, Depends
from models.film import FilmCreate, FilmResponse
from services.film_service import FilmService
from dependencies import get_film_service

router = APIRouter(prefix="/films", tags=["films"])


@router.get("/", response_model=list[FilmResponse])
async def get_all(service: FilmService = Depends(get_film_service)):
    """GET /films — Todas las películas."""
    return await service.get_all()


@router.post("/", response_model=FilmResponse, status_code=201)
async def create(film: FilmCreate, service: FilmService = Depends(get_film_service)):
    """POST /films — Crear una película."""
    return await service.create(film.model_dump())


@router.delete("/{id}")
async def delete(id: str, service: FilmService = Depends(get_film_service)):
    """DELETE /films/{id} — Eliminar una película."""
    await service.delete(id)
    return {"detail": "Película eliminada"}
```

### `backend/routes/playback.py`

```python
from fastapi import APIRouter, Depends
from services.playback_service import PlaybackService
from dependencies import get_playback_service

router = APIRouter(prefix="/playback", tags=["playback"])


@router.post("/game/{nombre}/{consola}")
async def play_game(nombre: str, consola: str,
                    service: PlaybackService = Depends(get_playback_service)):
    """
    POST /playback/game/Crash/ps1 — Iniciar un juego.
    El service valida, marca en BBDD y publica evento Redis.
    """
    return await service.play_game(nombre, consola)


@router.post("/film/{nombre}")
async def play_film(nombre: str,
                    service: PlaybackService = Depends(get_playback_service)):
    """POST /playback/film/Inception — Iniciar una película."""
    return await service.play_film(nombre)


@router.post("/stop")
async def stop(service: PlaybackService = Depends(get_playback_service)):
    """POST /playback/stop — Parar toda la reproducción."""
    await service.stop()
    return {"status": "stopped"}


@router.get("/current")
async def current(service: PlaybackService = Depends(get_playback_service)):
    """
    GET /playback/current — Qué se está reproduciendo ahora.
    Devuelve: {"type": "game|film|none", "data": {...} | null}
    """
    return await service.get_current()


@router.get("/trailer")
async def random_trailer(service: PlaybackService = Depends(get_playback_service)):
    """GET /playback/trailer — Un trailer aleatorio."""
    return await service.get_random_trailer()
```

### `backend/routes/health.py`

```python
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    """
    GET /health — Endpoint de salud.

    Sirve para verificar que el backend está arrancado y respondiendo.
    Docker, Kubernetes o cualquier sistema de monitorización puede hacer
    ping a este endpoint periódicamente.
    """
    return {"status": "ok", "service": "arcadiax-backend"}
```

---

## 3.8 Inyección de dependencias — `backend/dependencies.py`

```python
from database import db
from config import settings
from repositories.videogame_repo import VideogameRepository
from repositories.film_repo import FilmRepository
from services.videogame_service import VideogameService
from services.film_service import FilmService
from services.playback_service import PlaybackService
from events.publisher import EventPublisher

"""
Este archivo es la "fábrica" del backend. Crea las instancias de todo
y las conecta entre sí.

El flujo de creación es:
1. Crear los repositories (necesitan la colección de MongoDB)
2. Crear el event publisher (necesita la URL de Redis)
3. Crear los services (necesitan los repositories y el publisher)
4. Las funciones get_*_service() se usan con Depends() en las rutas
"""

# ── Repositories ──
# Cada uno recibe su colección de MongoDB
videogame_repo = VideogameRepository(db["videogames"])  # Colección "videogames"
film_repo = FilmRepository(db["films"])                  # Colección "films"

# ── Event Publisher ──
event_publisher = EventPublisher(settings.REDIS_URL)

# ── Services ──
videogame_service = VideogameService(videogame_repo)
film_service = FilmService(film_repo)
playback_service = PlaybackService(videogame_repo, film_repo, event_publisher)


def get_videogame_service() -> VideogameService:
    """FastAPI llama a esta función cuando una ruta necesita el service."""
    return videogame_service


def get_film_service() -> FilmService:
    return film_service


def get_playback_service() -> PlaybackService:
    return playback_service
```

---

## 3.9 Entrypoint — `backend/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes import videogames, films, playback, health

# Crea la aplicación FastAPI
app = FastAPI(title="ArcadiaX API", version="2.0.0")

# ── CORS Middleware ──
# CORS (Cross-Origin Resource Sharing) permite que el frontend
# (que corre en localhost:3000) haga peticiones al backend (localhost:8000).
# Sin esto, el navegador bloquea las peticiones por seguridad.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # Permite cualquier origen (en producción, poner la URL del frontend)
    allow_credentials=True,      # Permite enviar cookies
    allow_methods=["*"],         # Permite todos los métodos HTTP (GET, POST, PUT, DELETE)
    allow_headers=["*"],         # Permite todos los headers
)

# ── Registrar routers ──
# Cada router agrupa los endpoints de un módulo.
# include_router los monta en la aplicación.
app.include_router(health.router)       # GET /health
app.include_router(videogames.router)   # /videogames/*
app.include_router(films.router)        # /films/*
app.include_router(playback.router)     # /playback/*

# ── Arranque ──
if __name__ == "__main__":
    import uvicorn
    # uvicorn es el servidor ASGI que ejecuta la app FastAPI.
    # reload=True: reinicia automáticamente cuando detecta cambios en el código.
    # Útil en desarrollo, se quita en producción.
    uvicorn.run("main:app", host=settings.BACKEND_HOST,
                port=settings.BACKEND_PORT, reload=True)
```

**Al arrancar el backend:**
- Abre `http://localhost:8000/docs` → Swagger con todos los endpoints
- Abre `http://localhost:8000/health` → `{"status": "ok"}`

---

## 3.10 Dockerfile del backend — `backend/Dockerfile`

```dockerfile
# Imagen base: Python 3.12 versión ligera (slim = sin extras innecesarios)
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar primero solo requirements.txt
# Docker cachea capas: si requirements.txt no cambia, no reinstala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Comando que se ejecuta cuando arranca el contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# PARTE 4: ARCADE ENGINE — Motor del arcade

El arcade engine es el programa que controla el hardware de la máquina arcade:
abre emuladores, reproduce trailers, lee botones y gestiona el estado del sistema.

---

## 4.1 Configuración — `arcade/config.py`

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración del arcade engine.
    Lee del .env las rutas a emuladores y contenido.
    """
    REDIS_URL: str = "redis://localhost:6379"
    RETROARCH_PATH: str = "/Applications/RetroArch.app/Contents/MacOS/RetroArch"
    PPSSPP_PATH: str = "/Applications/PPSSPP.app/Contents/MacOS/PPSSPP"
    ROMS_PATH: str = "~/roms"
    TRAILERS_PATH: str = "~/trailers"
    MEDIA_PLAYER: str = "mpv"      # mpv o vlc

    class Config:
        env_file = ".env"


settings = Settings()
```

---

## 4.2 Máquina de estados — `arcade/playback/state_machine.py`

```python
from enum import Enum
import logging

log = logging.getLogger("arcadiax.state")


class State(Enum):
    """
    Los 6 estados posibles del arcade.

    IDLE      → Encendido pero sin actividad
    TRAILER   → Reproduciendo trailers en bucle (nadie juega)
    SELECTING → Pantalla de selección de juego (alguien pulsó un botón o abrió la web)
    LOADING   → Cargando el emulador con el juego elegido
    PLAYING   → Jugando
    SAVING    → Auto-guardando partida (vuelve a PLAYING automáticamente)
    """
    IDLE = "idle"
    TRAILER = "trailer"
    SELECTING = "selecting"
    LOADING = "loading"
    PLAYING = "playing"
    SAVING = "saving"


class ArcadeStateMachine:
    """
    Controla las transiciones entre estados.

    Solo permite transiciones válidas. Si alguien intenta ir de TRAILER
    a SAVING directamente, la máquina lo rechaza y registra un warning.

    Esto previene estados inconsistentes que en la v1 podían ocurrir
    cuando los ifs encadenados no cubrían todos los casos.
    """

    def __init__(self):
        self.state = State.IDLE

        # Mapa de transiciones válidas: estado_actual → [estados_permitidos]
        self._transitions = {
            State.IDLE: [State.TRAILER, State.SELECTING],
            #  IDLE puede ir a TRAILER (30s sin actividad) o SELECTING (alguien interactúa)

            State.TRAILER: [State.IDLE, State.SELECTING],
            #  TRAILER puede volver a IDLE o ir a SELECTING (alguien interactúa)

            State.SELECTING: [State.LOADING, State.IDLE],
            #  SELECTING puede ir a LOADING (elige juego) o volver a IDLE (timeout 60s)

            State.LOADING: [State.PLAYING, State.IDLE],
            #  LOADING puede ir a PLAYING (emulador arrancó) o IDLE (falló)

            State.PLAYING: [State.SAVING, State.IDLE],
            #  PLAYING puede ir a SAVING (auto-guardado) o IDLE (emulador cerrado)

            State.SAVING: [State.PLAYING, State.IDLE],
            #  SAVING vuelve a PLAYING (guardado completado) o IDLE (si falla)
        }

    def transition(self, new_state: State) -> bool:
        """
        Intenta cambiar de estado. Devuelve True si la transición es válida.

        Ejemplo:
            sm = ArcadeStateMachine()            # Estado: IDLE
            sm.transition(State.SELECTING)        # → True, ahora es SELECTING
            sm.transition(State.SAVING)           # → False, SELECTING no puede ir a SAVING
        """
        if new_state not in self._transitions.get(self.state, []):
            log.warning(f"Transición inválida: {self.state} → {new_state}")
            return False
        log.info(f"Estado: {self.state.value} → {new_state.value}")
        self.state = new_state
        return True

    @property
    def is_idle(self):
        """¿Está en reposo?"""
        return self.state == State.IDLE

    @property
    def is_selecting(self):
        """¿Está en pantalla de selección?"""
        return self.state == State.SELECTING

    @property
    def is_playing(self):
        """¿Está jugando? (incluye SAVING porque sigue jugando mientras guarda)"""
        return self.state in (State.PLAYING, State.SAVING)
```

---

## 4.3 Drivers de emuladores — `arcade/emulators/`

En la v1, los emuladores estaban hardcodeados como nombres de `.exe`. En la v2, cada emulador implementa una interfaz común.

### `arcade/emulators/base.py` — Interfaz base

```python
from abc import ABC, abstractmethod


class EmulatorDriver(ABC):
    """
    Clase abstracta que define la interfaz de un emulador.

    ABC (Abstract Base Class) obliga a que cualquier driver que herede
    de aquí implemente TODOS los métodos marcados con @abstractmethod.
    Si no los implementa, Python lanza un error al instanciar.

    Esto garantiza que todos los emuladores se usan de la misma forma:
        driver = get_driver("ps1")
        await driver.launch("/roms/crash.bin")
        if await driver.is_running():
            await driver.save_state()
        await driver.terminate()
    """

    @abstractmethod
    async def launch(self, rom_path: str) -> bool:
        """Lanza el emulador con una ROM. Devuelve True si arrancó bien."""
        pass

    @abstractmethod
    async def is_running(self) -> bool:
        """¿El emulador sigue ejecutándose?"""
        pass

    @abstractmethod
    async def terminate(self):
        """Cierra el emulador."""
        pass

    @abstractmethod
    async def save_state(self):
        """Guarda el estado de la partida (save state)."""
        pass

    @abstractmethod
    async def load_state(self):
        """Carga el último estado guardado."""
        pass
```

### `arcade/emulators/retroarch.py` — Driver RetroArch (multi-consola)

```python
import asyncio
import shutil
from arcade.emulators.base import EmulatorDriver


class RetroArchDriver(EmulatorDriver):
    """
    Driver para RetroArch.

    RetroArch es un frontend que unifica muchos emuladores bajo una interfaz común.
    Cada emulador real (snes9x, nestopia, etc.) se carga como un "core".

    Ventaja: en vez de tener un driver para cada emulador, RetroArch cubre
    la mayoría de consolas con un solo programa. Solo cambia el core.
    """

    # Mapeo: nombre de consola → core de RetroArch
    CORES = {
        "snes": "snes9x_libretro",              # Super Nintendo
        "nes": "nestopia_libretro",              # Nintendo Entertainment System
        "gba": "mgba_libretro",                  # Game Boy Advance
        "megadrive": "genesis_plus_gx_libretro", # Sega Mega Drive / Genesis
        "n64": "mupen64plus_next_libretro",      # Nintendo 64
        "ps1": "pcsx_rearmed_libretro",          # PlayStation 1
        "arcade": "mame_libretro",               # Máquinas arcade (MAME)
    }

    def __init__(self, consola: str, retroarch_path: str = None):
        self.consola = consola
        self.core = self.CORES.get(consola)     # Busca el core para esta consola
        # shutil.which busca "retroarch" en el PATH del sistema
        self.retroarch_path = retroarch_path or shutil.which("retroarch")
        self.process = None                      # Referencia al proceso del emulador

    async def launch(self, rom_path: str) -> bool:
        """
        Lanza RetroArch con el core y la ROM.

        asyncio.create_subprocess_exec ejecuta el comando de forma asíncrona.
        No bloquea el programa mientras el emulador está abierto.

        -L: especifica el core (librería) a usar

        stdout/stderr DEVNULL: descarta la salida del emulador para no llenar los logs.
        """
        if not self.core or not self.retroarch_path:
            return False
        self.process = await asyncio.create_subprocess_exec(
            self.retroarch_path, "-L", self.core, rom_path,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )
        # returncode es None mientras el proceso sigue corriendo
        return self.process.returncode is None

    async def is_running(self) -> bool:
        """Si returncode sigue siendo None, el emulador sigue abierto."""
        return self.process is not None and self.process.returncode is None

    async def terminate(self):
        """Cierra el emulador. terminate() envía SIGTERM (cierre limpio)."""
        if self.process and self.process.returncode is None:
            self.process.terminate()
            await self.process.wait()  # Espera a que el proceso termine

    async def save_state(self):
        # RetroArch soporta save states vía su command interface UDP.
        # Se puede implementar enviando comandos UDP al puerto de RetroArch.
        pass

    async def load_state(self):
        pass
```

### `arcade/emulators/ppsspp.py` — Driver PPSSPP (PSP)

```python
import asyncio
import shutil
from arcade.emulators.base import EmulatorDriver


class PPSSPPDriver(EmulatorDriver):
    """
    Driver específico para PPSSPP (emulador de PSP).

    PPSSPP necesita su propio driver porque:
    - No se integra bien con RetroArch
    - Tiene su propia API HTTP para control remoto
    - Los save states funcionan diferente (F2/F4 en vez de UDP)
    """

    def __init__(self, consola: str, ppsspp_path: str = None):
        # Busca "ppsspp" o "PPSSPP" en el PATH del sistema
        self.ppsspp_path = ppsspp_path or shutil.which("ppsspp") or shutil.which("PPSSPP")
        self.process = None

    async def launch(self, rom_path: str) -> bool:
        """Lanza PPSSPP con la ROM directamente como argumento."""
        if not self.ppsspp_path:
            return False
        self.process = await asyncio.create_subprocess_exec(
            self.ppsspp_path, rom_path,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )
        return self.process.returncode is None

    async def is_running(self) -> bool:
        return self.process is not None and self.process.returncode is None

    async def terminate(self):
        if self.process and self.process.returncode is None:
            self.process.terminate()
            await self.process.wait()

    async def save_state(self):
        # PPSSPP: se puede usar su API HTTP (si está habilitada)
        # o simular la tecla F2 con pyautogui (como en la v1)
        pass

    async def load_state(self):
        # Simular F4 o usar API HTTP
        pass
```

### `arcade/emulators/registry.py` — Registro de drivers

```python
from arcade.emulators.retroarch import RetroArchDriver
from arcade.emulators.ppsspp import PPSSPPDriver
from arcade.emulators.base import EmulatorDriver

# Mapeo: nombre de consola → clase del driver
# Para añadir una consola nueva, solo hay que añadir una línea aquí.
EMULATOR_MAP = {
    "snes": RetroArchDriver,
    "nes": RetroArchDriver,
    "gba": RetroArchDriver,
    "megadrive": RetroArchDriver,
    "n64": RetroArchDriver,
    "ps1": RetroArchDriver,
    "arcade": RetroArchDriver,
    "psp": PPSSPPDriver,        # PSP usa su propio driver
}


def get_driver(consola: str, **kwargs) -> EmulatorDriver:
    """
    Devuelve el driver correcto para una consola.

    Uso:
        driver = get_driver("ps1")       # → RetroArchDriver(consola="ps1")
        driver = get_driver("psp")       # → PPSSPPDriver(consola="psp")
        driver = get_driver("dreamcast") # → ValueError (no hay driver)

    **kwargs permite pasar parámetros extra al constructor del driver,
    como retroarch_path o ppsspp_path.
    """
    driver_class = EMULATOR_MAP.get(consola.lower())
    if not driver_class:
        raise ValueError(f"No hay driver para la consola: {consola}")
    return driver_class(consola=consola, **kwargs)
```

---

## 4.4 Controladores — `arcade/playback/`

### `arcade/playback/game_controller.py`

```python
import logging
from arcade.emulators.registry import get_driver
from arcade.emulators.base import EmulatorDriver

log = logging.getLogger("arcadiax.game")


class GameController:
    """
    Controla la ejecución de juegos.

    Abstrae el proceso de: buscar el driver → lanzar emulador → monitorizar → cerrar.
    El ArcadeEngine usa este controller sin preocuparse de qué emulador es.
    """

    def __init__(self):
        self.current_driver: EmulatorDriver = None  # Driver del juego en ejecución

    async def launch(self, consola: str, rom_path: str) -> bool:
        """
        Lanza un juego.
        1. Busca el driver correcto para la consola
        2. Llama a driver.launch() con la ruta de la ROM
        3. Devuelve True si arrancó bien, False si falló
        """
        try:
            self.current_driver = get_driver(consola)
            success = await self.current_driver.launch(rom_path)
            if success:
                log.info(f"Juego lanzado: {rom_path} ({consola})")
            else:
                log.error(f"Fallo al lanzar: {rom_path} ({consola})")
            return success
        except ValueError as e:
            # get_driver lanza ValueError si no hay driver para esa consola
            log.error(str(e))
            return False

    async def is_running(self) -> bool:
        """¿El emulador sigue corriendo?"""
        if not self.current_driver:
            return False
        return await self.current_driver.is_running()

    async def terminate(self):
        """Cierra el emulador actual."""
        if self.current_driver:
            await self.current_driver.terminate()
            log.info("Emulador cerrado")
            self.current_driver = None

    async def save_state(self):
        """Guarda el estado de la partida actual."""
        if self.current_driver:
            await self.current_driver.save_state()
            log.info("Estado guardado")
```

### `arcade/playback/media_controller.py`

```python
import asyncio
import os
import random
import logging

log = logging.getLogger("arcadiax.media")


class MediaController:
    """
    Controla la reproducción de trailers y películas.
    Usa mpv o VLC como reproductor externo.
    """

    def __init__(self, trailers_path: str, player: str = "mpv"):
        self.trailers_path = os.path.expanduser(trailers_path)  # ~/trailers → /home/user/trailers
        self.player = player       # "mpv" o "vlc"
        self.process = None        # Proceso del reproductor

    async def play_random_trailer(self):
        """
        Reproduce un trailer aleatorio de la carpeta de trailers.

        1. Lista todos los vídeos de la carpeta
        2. Elige uno al azar
        3. Lo abre con mpv/VLC en pantalla completa
        """
        if not os.path.isdir(self.trailers_path):
            log.warning(f"Directorio de trailers no existe: {self.trailers_path}")
            return

        # Filtrar solo archivos de vídeo
        videos = [
            f for f in os.listdir(self.trailers_path)
            if f.endswith((".mp4", ".mkv", ".avi", ".mov"))
        ]
        if not videos:
            log.warning("No hay trailers disponibles")
            return

        trailer = os.path.join(self.trailers_path, random.choice(videos))
        log.info(f"Reproduciendo trailer: {trailer}")

        # Argumentos según el reproductor
        args = [self.player, "--fullscreen", trailer]
        if self.player == "mpv":
            args = [self.player, "--fs", "--no-terminal", trailer]
            # --fs: fullscreen
            # --no-terminal: no muestra info en la terminal

        self.process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )

    async def play_url(self, url: str):
        """Reproduce un vídeo por ruta o URL (para películas)."""
        log.info(f"Reproduciendo: {url}")
        args = [self.player, "--fs", "--no-terminal", url] if self.player == "mpv" \
            else [self.player, "--fullscreen", url]
        self.process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )

    async def is_playing(self) -> bool:
        """¿El reproductor sigue corriendo?"""
        return self.process is not None and self.process.returncode is None

    async def stop(self):
        """Para el reproductor."""
        if self.process and self.process.returncode is None:
            self.process.terminate()
            await self.process.wait()
            log.info("Reproductor parado")
            self.process = None
```

---

## 4.5 Input arcade — `arcade/input/arcade_input.py`

```python
import asyncio
import logging

log = logging.getLogger("arcadiax.input")


class ArcadeInputReader:
    """
    Lee los botones y joystick de la máquina arcade física.

    El encoder USB del arcade (la placa que conecta los botones al PC)
    se comporta como un joystick/gamepad. pygame lo detecta y lee sus inputs.

    Cada botón físico se mapea a una acción:
    - Botón 0 → "select" (entrar a selección de juego)
    - Botón 1 → "back" (volver / salir)
    - Botón 2 → "confirm" (confirmar selección)

    Cuando se detecta un input, se publica un evento Redis.
    El ArcadeEngine lo recibe y actúa según el estado actual.
    """

    BUTTON_MAP = {
        0: "select",        # Primer botón del encoder
        1: "back",          # Segundo botón
        2: "confirm",       # Tercer botón
    }

    def __init__(self, event_publisher):
        self.events = event_publisher
        self.running = False

    async def start(self):
        """
        Inicia la lectura de inputs del arcade.
        Se ejecuta en un bucle infinito escuchando eventos de pygame.
        """
        try:
            import pygame
            pygame.init()
            pygame.joystick.init()
        except ImportError:
            log.warning("pygame no instalado, input arcade deshabilitado")
            return

        if pygame.joystick.get_count() == 0:
            log.warning("No se detectó joystick/encoder arcade USB")
            # No sale del bucle — sigue corriendo para no romper asyncio.gather
            while True:
                await asyncio.sleep(10)

        joystick = pygame.joystick.Joystick(0)   # Primer joystick detectado
        joystick.init()
        log.info(f"Arcade input detectado: {joystick.get_name()}")

        self.running = True
        while self.running:
            for event in pygame.event.get():
                # Botón pulsado
                if event.type == pygame.JOYBUTTONDOWN:
                    action = self.BUTTON_MAP.get(event.button)
                    if action:
                        await self._handle_action(action)
                # Joystick movido (eje X o Y)
                elif event.type == pygame.JOYAXISMOTION:
                    if abs(event.value) > 0.5:   # Umbral para evitar inputs fantasma
                        await self._handle_action("select")

            await asyncio.sleep(0.05)  # 20 comprobaciones por segundo

    async def _handle_action(self, action: str):
        """Convierte la acción en un evento Redis."""
        from shared.events import Events
        log.info(f"Input arcade: {action}")
        event_map = {
            "select": Events.ARCADE_BUTTON_SELECT,
            "back": Events.ARCADE_BUTTON_BACK,
            "confirm": Events.ARCADE_BUTTON_CONFIRM,
        }
        event = event_map.get(action)
        if event:
            await self.events.publish(event, {})

    def stop(self):
        self.running = False
```

---

## 4.6 Eventos del arcade — `arcade/events/`

### `arcade/events/publisher.py`

Idéntico al del backend. Publica eventos en el canal "arcadiax" de Redis.

```python
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
```

### `arcade/events/listener.py`

```python
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
        await listener.listen()  # Bloquea escuchando indefinidamente
    """

    def __init__(self, handlers: dict, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.handlers = handlers   # {nombre_evento: función_async}

    async def listen(self):
        """
        Escucha eventos indefinidamente.

        pubsub.subscribe("arcadiax") se suscribe al canal.
        async for message in pubsub.listen() itera cada vez que llega un mensaje.

        Los mensajes tienen un campo "type":
        - "subscribe": confirmación de suscripción (lo ignoramos)
        - "message": un evento real (lo procesamos)
        """
        pubsub = self.redis.pubsub()
        await pubsub.subscribe("arcadiax")
        log.info("Escuchando eventos en canal 'arcadiax'")

        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            try:
                payload = json.loads(message["data"])
                event = payload["event"]    # Nombre del evento
                data = payload["data"]      # Datos del evento

                handler = self.handlers.get(event)
                if handler:
                    await handler(data)     # Ejecuta la función asociada al evento
            except (json.JSONDecodeError, KeyError) as e:
                log.error(f"Error procesando evento: {e}")
```

---

## 4.7 Motor principal — `arcade/main.py`

```python
import asyncio
import logging
from arcade.playback.state_machine import ArcadeStateMachine, State
from arcade.playback.game_controller import GameController
from arcade.playback.media_controller import MediaController
from arcade.input.arcade_input import ArcadeInputReader
from arcade.events.listener import EventListener
from arcade.events.publisher import EventPublisher
from shared.events import Events
from arcade.config import settings

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] %(name)s | %(levelname)s | %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger("arcadiax")


class ArcadeEngine:
    """
    Motor principal del arcade. Orquesta todo:
    - Escucha eventos (del backend y del input físico)
    - Gestiona la máquina de estados
    - Controla emuladores y reproductor de trailers
    - Monitoriza que todo siga corriendo

    Ejecuta 3 tareas en paralelo con asyncio.gather:
    1. EventListener: escucha eventos Redis
    2. ArcadeInputReader: lee botones del arcade
    3. monitor_loop: comprobación cada segundo (trailers, auto-guardado, etc.)
    """

    def __init__(self):
        self.sm = ArcadeStateMachine()                                # Máquina de estados
        self.events = EventPublisher(settings.REDIS_URL)              # Para publicar eventos
        self.game = GameController()                                  # Controla emuladores
        self.media = MediaController(settings.TRAILERS_PATH, settings.MEDIA_PLAYER)  # Trailers
        self.arcade_input = ArcadeInputReader(self.events)            # Botones físicos
        self.selecting_timer = None                                   # Timer de timeout

    async def start(self):
        """Arranca el motor. Registra handlers y lanza las 3 tareas."""
        log.info("ArcadiaX Engine v2 iniciado")

        # Mapa: evento → función que lo maneja
        handlers = {
            Events.ARCADE_BUTTON_SELECT: self.on_select,    # Botón select del arcade
            Events.WEB_SELECT_REQUEST: self.on_select,      # Acceso desde la web
            Events.GAME_PLAY: self.on_game_chosen,          # Usuario eligió un juego
            Events.FILM_PLAY: self.on_film_chosen,          # Usuario eligió una película
            Events.ARCADE_BUTTON_BACK: self.on_back,        # Botón back
            Events.PLAYBACK_STOP: self.on_stop,             # Parar todo
        }
        listener = EventListener(handlers, settings.REDIS_URL)

        # asyncio.gather ejecuta las 3 tareas en paralelo.
        # Si una falla, las demás siguen corriendo.
        await asyncio.gather(
            listener.listen(),          # Tarea 1: escuchar eventos Redis
            self.arcade_input.start(),  # Tarea 2: leer botones del arcade
            self.monitor_loop(),        # Tarea 3: monitorización cada segundo
        )

    # ── HANDLERS DE EVENTOS ──────────────────────────────

    async def on_select(self, data: dict):
        """
        Alguien quiere seleccionar un juego (botón arcade O acceso web).

        Solo actúa si estamos en IDLE o TRAILER.
        Para los trailers, cambia a SELECTING e inicia un timer de 60s.
        """
        if self.sm.state in (State.IDLE, State.TRAILER):
            await self.media.stop()                              # Para trailers
            self.sm.transition(State.SELECTING)
            await self.events.publish(Events.STATE_CHANGED, {"state": "selecting"})
            # Timer: si en 60s no elige, vuelve a IDLE
            self.selecting_timer = asyncio.create_task(self._selecting_timeout(60))

    async def on_game_chosen(self, data: dict):
        """
        Usuario eligió un juego. Intenta cargarlo.

        data contiene: {"nombre": "Crash", "consola": "ps1", "ubicacion": "/roms/crash.bin"}
        """
        if not self.sm.transition(State.LOADING):
            return  # Transición no válida desde el estado actual

        # Cancelar el timer de selección
        if self.selecting_timer:
            self.selecting_timer.cancel()

        # Lanzar el emulador
        success = await self.game.launch(data["consola"], data["ubicacion"])
        if success:
            self.sm.transition(State.PLAYING)
            await self.events.publish(Events.STATE_CHANGED, {"state": "playing", "data": data})
        else:
            # Si falla, volver a IDLE
            self.sm.transition(State.IDLE)
            await self.events.publish(Events.STATE_CHANGED, {"state": "idle", "error": "fallo al lanzar"})

    async def on_film_chosen(self, data: dict):
        """Usuario eligió una película. Abrirla con mpv/VLC."""
        if not self.sm.transition(State.LOADING):
            return
        if self.selecting_timer:
            self.selecting_timer.cancel()

        await self.media.play_url(data["ubicacion"])
        self.sm.transition(State.PLAYING)
        await self.events.publish(Events.STATE_CHANGED, {"state": "playing", "data": data})

    async def on_back(self, data: dict):
        """
        Botón back: comportamiento depende del estado actual.
        - En SELECTING → vuelve a IDLE (cancelar selección)
        - En PLAYING → cierra emulador y vuelve a IDLE
        """
        if self.sm.is_selecting:
            if self.selecting_timer:
                self.selecting_timer.cancel()
            self.sm.transition(State.IDLE)
            await self.events.publish(Events.STATE_CHANGED, {"state": "idle"})
        elif self.sm.is_playing:
            await self.game.terminate()
            await self.media.stop()
            self.sm.transition(State.IDLE)
            await self.events.publish(Events.STATE_CHANGED, {"state": "idle"})

    async def on_stop(self, data: dict):
        """Parar todo (viene del backend cuando alguien hace POST /playback/stop)."""
        await self.game.terminate()
        await self.media.stop()
        self.sm.transition(State.IDLE)

    # ── LOOP DE MONITORIZACIÓN ───────────────────────────

    async def monitor_loop(self):
        """
        Se ejecuta cada segundo. Comprueba:

        En IDLE:
        - Si lleva 30s sin actividad → poner trailers (IDLE → TRAILER)

        En TRAILER:
        - Si el trailer actual terminó → poner otro

        En PLAYING:
        - ¿Se cerró el emulador? → volver a IDLE
        - ¿Han pasado 30s? → auto-guardado (PLAYING → SAVING → PLAYING)
        """
        idle_count = 0     # Segundos en IDLE sin actividad
        save_count = 0     # Segundos desde el último auto-guardado

        while True:
            state = self.sm.state

            if state == State.IDLE:
                idle_count += 1
                if idle_count >= 30:
                    self.sm.transition(State.TRAILER)
                    await self.media.play_random_trailer()
                    idle_count = 0

            elif state == State.TRAILER:
                idle_count = 0
                # Si el trailer terminó, poner otro
                if not await self.media.is_playing():
                    await self.media.play_random_trailer()

            elif state == State.PLAYING:
                idle_count = 0
                save_count += 1

                # ¿El emulador/reproductor se cerró?
                if not await self.game.is_running() and not await self.media.is_playing():
                    log.info("Reproducción terminada, volviendo a IDLE")
                    self.sm.transition(State.IDLE)
                    await self.events.publish(Events.STATE_CHANGED, {"state": "idle"})
                    save_count = 0

                # Auto-guardado cada 30 segundos (solo para juegos, no películas)
                elif save_count >= 30 and await self.game.is_running():
                    self.sm.transition(State.SAVING)
                    await self.game.save_state()
                    self.sm.transition(State.PLAYING)
                    save_count = 0
            else:
                idle_count = 0

            await asyncio.sleep(1)  # Cada segundo

    async def _selecting_timeout(self, seconds: int):
        """Si no elige juego en X segundos, volver a IDLE."""
        await asyncio.sleep(seconds)
        if self.sm.is_selecting:
            log.info("Timeout de selección")
            self.sm.transition(State.IDLE)
            await self.events.publish(Events.STATE_CHANGED, {"state": "idle"})


# ── ARRANQUE ──
if __name__ == "__main__":
    engine = ArcadeEngine()
    asyncio.run(engine.start())
```

---

# PARTE 5: FRONTEND — Interfaz web con React

El frontend es una app React con Tailwind CSS. Se puede usar desde:
- El monitor del arcade (pantalla completa, navegar con joystick)
- El móvil o PC (navegador normal, navegar con táctil/ratón)

Está organizado en 4 capas:
```
config/     → Configuración (URL del backend)
services/   → Llamadas HTTP al backend
hooks/      → Lógica React (loading, error, datos)
components/ → Interfaz visual (lo que se ve)
pages/      → Páginas completas (combinan componentes)
```

---

## 5.1 Configuración — `frontend/package.json`

```json
{
  "name": "arcadiax-frontend",
  "version": "2.0.0",
  "private": true,
  "dependencies": {
    "axios": "^1.7.0",              // Cliente HTTP para llamar al backend
    "react": "^18.3.0",             // Librería principal
    "react-dom": "^18.3.0",         // Renderizado en el navegador
    "react-router-dom": "^6.26.0",  // Navegación entre páginas (SPA)
    "react-scripts": "5.0.1"        // Scripts de Create React App
  },
  "devDependencies": {
    "tailwindcss": "^3.4.0",        // Framework CSS (clases utilitarias)
    "autoprefixer": "^10.4.0",      // Añade prefijos CSS para compatibilidad
    "postcss": "^8.4.0"             // Procesador CSS (necesario para Tailwind)
  }
}
```

## 5.2 Tailwind config — `frontend/tailwind.config.js`

```javascript
module.exports = {
  // Tailwind escanea estos archivos para saber qué clases CSS incluir
  content: ["./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      // Fuentes personalizadas para la estética arcade
      fontFamily: {
        arcade: ['"Press Start 2P"', "monospace"],  // Fuente pixelada retro
        orbitron: ["Orbitron", "sans-serif"],        // Fuente futurista
      },
      // Colores neón del tema arcade
      colors: {
        neon: {
          cyan: "#00f5ff",
          pink: "#ff00e5",
          yellow: "#ffe600",
          green: "#00ff66",
          red: "#ff1a1a",
        },
      },
      // Animaciones custom
      animation: {
        "pulse-neon": "pulseNeon 2s ease-in-out infinite",  // Parpadeo neón
        "fade-in": "fadeIn 0.3s ease-out",                  // Entrada suave
      },
      keyframes: {
        pulseNeon: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.7" },
        },
        fadeIn: {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};
```

## 5.3 CSS global — `frontend/src/index.css`

```css
@tailwind base;        /* Reset CSS de Tailwind */
@tailwind components;  /* Clases de componentes de Tailwind */
@tailwind utilities;   /* Clases utilitarias (text-white, flex, etc.) */

body {
  margin: 0;
  background-color: #000;   /* Fondo negro por defecto */
  color: #fff;
  overflow-x: hidden;       /* Evita scroll horizontal */
}

/* Efecto neón: sombra de texto que simula luz de neón */
.neon-text-cyan {
  text-shadow: 0 0 4px #00f5ff, 0 0 10px #00f5ff, 0 0 20px #00b4d8;
}

.neon-text-yellow {
  text-shadow: 0 0 4px #ffe600, 0 0 10px #ffe600, 0 0 20px #ccb800;
}

.neon-text-red {
  text-shadow: 0 0 4px #ff1a1a, 0 0 10px #ff1a1a, 0 0 20px #ff0000;
}

.neon-text-green {
  text-shadow: 0 0 4px #00ff66, 0 0 10px #00ff66, 0 0 20px #00cc44;
}

/* Scrollbar personalizada acorde al tema oscuro */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #555; }
```

## 5.4 API centralizada — `frontend/src/config/api.js`

```javascript
import axios from "axios";

// Crea una instancia de axios con configuración base.
// Todas las llamadas al backend usan esta instancia.
// Si cambias la URL del backend, lo cambias SOLO AQUÍ.
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000",
  timeout: 10000,   // 10 segundos máximo por petición
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
```

## 5.5 Services — Llamadas al backend

### `frontend/src/services/videogameService.js`

```javascript
import api from "../config/api";

// Objeto con todas las operaciones de videojuegos.
// Los componentes y hooks llaman a estos métodos sin saber nada de URLs o axios.
const videogameService = {
  getAll: () => api.get("/videogames"),
  getById: (id) => api.get(`/videogames/${id}`),
  getConsoles: () => api.get("/videogames/consoles"),
  getByConsole: (consola) => api.get(`/videogames/console/${consola}`),
  create: (data) => api.post("/videogames", data),
  update: (id, data) => api.put(`/videogames/${id}`, data),
  delete: (id) => api.delete(`/videogames/${id}`),
};

export default videogameService;
```

### `frontend/src/services/filmService.js`

```javascript
import api from "../config/api";

const filmService = {
  getAll: () => api.get("/films"),
  create: (data) => api.post("/films", data),
  delete: (id) => api.delete(`/films/${id}`),
};

export default filmService;
```

### `frontend/src/services/playbackService.js`

```javascript
import api from "../config/api";

const playbackService = {
  playGame: (nombre, consola) => api.post(`/playback/game/${nombre}/${consola}`),
  playFilm: (nombre) => api.post(`/playback/film/${nombre}`),
  stop: () => api.post("/playback/stop"),
  getCurrent: () => api.get("/playback/current"),
  getRandomTrailer: () => api.get("/playback/trailer"),
};

export default playbackService;
```

## 5.6 Hooks — Lógica React reutilizable

### `frontend/src/hooks/useVideogames.js`

```javascript
import { useState, useEffect, useCallback } from "react";
import videogameService from "../services/videogameService";

/**
 * Hook para cargar videojuegos.
 *
 * Uso en un componente:
 *   const { games, loading, error, refresh } = useVideogames("ps1");
 *
 * - games: array de juegos
 * - loading: true mientras carga
 * - error: mensaje de error si falla, null si todo OK
 * - refresh: función para recargar sin reload de página
 */
export function useVideogames(consola) {
  const [games, setGames] = useState([]);        // Lista de juegos
  const [loading, setLoading] = useState(true);  // ¿Está cargando?
  const [error, setError] = useState(null);      // Mensaje de error

  // useCallback memoriza la función para que no se recree en cada render.
  // Solo se recrea si cambia "consola".
  const fetch = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      // Si se pasa consola, filtra por ella. Si no, trae todos.
      const res = consola
        ? await videogameService.getByConsole(consola)
        : await videogameService.getAll();
      setGames(res.data);
    } catch (err) {
      // err.response?.data?.detail: mensaje de error del backend (FastAPI)
      setError(err.response?.data?.detail || "Error al cargar videojuegos");
    } finally {
      setLoading(false);   // Siempre desactiva loading, haya error o no
    }
  }, [consola]);

  // useEffect ejecuta fetch() cuando el componente se monta o cambia consola.
  useEffect(() => {
    fetch();
  }, [fetch]);

  return { games, loading, error, refresh: fetch };
}

/**
 * Hook para cargar la lista de consolas.
 * Uso: const { consoles, loading, error } = useConsoles();
 */
export function useConsoles() {
  const [consoles, setConsoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetch = async () => {
      try {
        setLoading(true);
        const res = await videogameService.getConsoles();
        setConsoles(res.data);
      } catch (err) {
        setError(err.response?.data?.detail || "Error al cargar consolas");
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, []);

  return { consoles, loading, error };
}
```

### `frontend/src/hooks/useFilms.js`

```javascript
import { useState, useEffect, useCallback } from "react";
import filmService from "../services/filmService";

/**
 * Hook para cargar películas.
 * Uso: const { films, loading, error, refresh } = useFilms();
 */
export function useFilms() {
  const [films, setFilms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetch = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await filmService.getAll();
      setFilms(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Error al cargar películas");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetch();
  }, [fetch]);

  return { films, loading, error, refresh: fetch };
}
```

### `frontend/src/hooks/usePlayback.js`

```javascript
import { useState, useCallback } from "react";
import playbackService from "../services/playbackService";

/**
 * Hook para controlar la reproducción.
 *
 * Uso:
 *   const { current, playGame, playFilm, stop, error } = usePlayback();
 *   await playGame("Crash", "ps1");   // Inicia un juego
 *   await stop();                      // Para todo
 *   current.type === "game"            // ¿Qué se está reproduciendo?
 */
export function usePlayback() {
  const [current, setCurrent] = useState({ type: "none", data: null });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchCurrent = useCallback(async () => {
    try {
      const res = await playbackService.getCurrent();
      setCurrent(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Error al obtener estado");
    }
  }, []);

  const playGame = useCallback(async (nombre, consola) => {
    try {
      setLoading(true);
      setError(null);
      await playbackService.playGame(nombre, consola);
      await fetchCurrent();    // Actualiza el estado después de iniciar
    } catch (err) {
      setError(err.response?.data?.detail || "Error al iniciar juego");
    } finally {
      setLoading(false);
    }
  }, [fetchCurrent]);

  const playFilm = useCallback(async (nombre) => {
    try {
      setLoading(true);
      setError(null);
      await playbackService.playFilm(nombre);
      await fetchCurrent();
    } catch (err) {
      setError(err.response?.data?.detail || "Error al iniciar película");
    } finally {
      setLoading(false);
    }
  }, [fetchCurrent]);

  const stop = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      await playbackService.stop();
      setCurrent({ type: "none", data: null });
    } catch (err) {
      setError(err.response?.data?.detail || "Error al parar");
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    current,
    loading,
    error,
    playGame,
    playFilm,
    stop,
    fetchCurrent,
    clearError: () => setError(null),
  };
}
```

## 5.7 Componentes de layout

### `frontend/src/components/layout/Navbar.jsx`

```jsx
import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";

// Definición de los items del menú como datos, no como HTML repetido.
// Si quieres añadir una página nueva, solo añades un objeto aquí.
const NAV_ITEMS = [
  { to: "/", label: "Inicio", color: "cyan" },
  { to: "/consolas", label: "Arcades", color: "yellow" },
  { to: "/peliculas", label: "Homeflix", color: "red" },
];

// Mapeo de color a clases Tailwind.
// Evita tener condicionales largos en el JSX.
const COLOR_MAP = {
  cyan: {
    border: "border-neon-cyan",
    text: "text-neon-cyan",
    hoverBg: "hover:bg-neon-cyan",
    activeBg: "bg-neon-cyan",
  },
  yellow: {
    border: "border-neon-yellow",
    text: "text-neon-yellow",
    hoverBg: "hover:bg-neon-yellow",
    activeBg: "bg-neon-yellow",
  },
  red: {
    border: "border-neon-red",
    text: "text-neon-red",
    hoverBg: "hover:bg-neon-red",
    activeBg: "bg-neon-red",
  },
};

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);      // Menú móvil abierto/cerrado
  const location = useLocation();                    // Ruta actual (para marcar activo)

  return (
    <nav className="fixed top-0 left-0 w-full bg-gradient-to-r from-gray-900 via-black to-gray-900 p-4 shadow-lg z-50">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="text-neon-cyan text-2xl md:text-3xl font-bold font-orbitron">
          ArcadiaX
        </Link>

        {/* Botón hamburguesa — solo visible en móvil (md:hidden) */}
        <button
          className="md:hidden text-white text-2xl hover:text-neon-cyan transition-colors"
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Menú"
        >
          {isOpen ? "✕" : "☰"}
        </button>

        {/* Menú desktop — oculto en móvil (hidden md:flex) */}
        <div className="hidden md:flex gap-3">
          {NAV_ITEMS.map((item) => {
            const colors = COLOR_MAP[item.color];
            const isActive = location.pathname === item.to;
            return (
              <Link
                key={item.to}
                to={item.to}
                className={`px-4 py-2 rounded-md border-2 text-sm font-arcade transition-all duration-300
                  ${colors.border} ${isActive ? `${colors.activeBg} text-black` : `${colors.text} ${colors.hoverBg} hover:text-black`}`}
              >
                {item.label}
              </Link>
            );
          })}
        </div>
      </div>

      {/* Menú móvil desplegable */}
      {isOpen && (
        <div className="md:hidden flex flex-col gap-3 mt-4 animate-fade-in">
          {NAV_ITEMS.map((item) => {
            const colors = COLOR_MAP[item.color];
            const isActive = location.pathname === item.to;
            return (
              <Link
                key={item.to}
                to={item.to}
                onClick={() => setIsOpen(false)}   // Cierra el menú al navegar
                className={`px-4 py-2 rounded-md border-2 text-sm font-arcade text-center transition-all duration-300
                  ${colors.border} ${isActive ? `${colors.activeBg} text-black` : `${colors.text} ${colors.hoverBg} hover:text-black`}`}
              >
                {item.label}
              </Link>
            );
          })}
        </div>
      )}
    </nav>
  );
}
```

### `frontend/src/components/layout/Layout.jsx`

```jsx
import React from "react";
import Navbar from "./Navbar";

/**
 * Componente wrapper que envuelve todas las páginas.
 * Incluye la Navbar y gestiona el fondo.
 *
 * Uso:
 *   <Layout backgroundImage="/assets/fondo/arcade.jpg">
 *     <h1>Contenido de la página</h1>
 *   </Layout>
 *
 * pt-20: padding-top de 80px para que el contenido no quede debajo de la Navbar fija.
 */
export default function Layout({ children, backgroundImage }) {
  return (
    <div
      className="min-h-screen bg-black"
      style={
        backgroundImage
          ? {
              backgroundImage: `url('${backgroundImage}')`,
              backgroundSize: "cover",
              backgroundPosition: "center",
              backgroundAttachment: "fixed",
            }
          : undefined
      }
    >
      <Navbar />
      <main className="pt-20 px-4 pb-8">{children}</main>
    </div>
  );
}
```

### `frontend/src/components/layout/Loading.jsx`

```jsx
import React from "react";

/**
 * Spinner de carga con estética neón.
 * Se muestra mientras los datos se están cargando del backend.
 *
 * En la v1 no había esto — el usuario veía una pantalla en blanco.
 */
export default function Loading({ text = "Cargando..." }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 animate-pulse-neon">
      {/* Spinner circular con borde cyan */}
      <div className="w-12 h-12 border-4 border-neon-cyan border-t-transparent rounded-full animate-spin mb-4" />
      <p className="text-neon-cyan font-arcade text-sm">{text}</p>
    </div>
  );
}
```

### `frontend/src/components/layout/ErrorMessage.jsx`

```jsx
import React from "react";

/**
 * Mensaje de error con botón de reintentar.
 * Se muestra cuando una llamada al backend falla.
 *
 * En la v1 los errores solo salían en console.error. El usuario no veía nada.
 */
export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <p className="text-neon-red font-arcade text-sm mb-4 text-center">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 border-2 border-neon-red text-neon-red rounded-md font-arcade text-xs hover:bg-neon-red hover:text-black transition-all"
        >
          Reintentar
        </button>
      )}
    </div>
  );
}
```

## 5.8 Componentes de contenido

### `frontend/src/components/videogames/ConsoleCard.jsx`

```jsx
import React from "react";
import { useNavigate } from "react-router-dom";

/**
 * Tarjeta de consola. Al hacer clic, navega a la lista de juegos de esa consola.
 *
 * Props:
 *   consola: string — nombre de la consola ("ps1", "snes", etc.)
 */
export default function ConsoleCard({ consola }) {
  const navigate = useNavigate();

  return (
    <button
      onClick={() => navigate(`/juegos/${consola.toLowerCase()}`)}
      className="w-full max-w-[160px] h-[180px] bg-neon-yellow hover:brightness-110 transition-all duration-300
        rounded-md shadow-md flex flex-col justify-between items-center p-2 border-2 border-yellow-600
        hover:scale-105 active:scale-95"
    >
      <div className="w-full h-1 bg-yellow-200 rounded-t-sm" />

      <div className="w-full h-[90px] flex items-center justify-center overflow-hidden rounded">
        <img
          src={`/assets/consolas/${encodeURIComponent(consola)}.jpg`}
          alt={consola}
          className="object-contain h-full w-full"
          onError={(e) => {
            // Si no encuentra la imagen de la consola, usa una genérica
            e.target.src = "/assets/consolas/default.jpg";
          }}
        />
      </div>

      <span className="text-black text-center text-xs font-bold font-arcade tracking-tight leading-tight">
        {consola.toUpperCase()}
      </span>
    </button>
  );
}
```

### `frontend/src/components/videogames/GameCard.jsx`

```jsx
import React from "react";

/**
 * Tarjeta de videojuego con forma de cartucho.
 *
 * Props:
 *   game: objeto con {nombre, consola, imagen, _id}
 *   onPlay: función(nombre, consola) — se llama al hacer clic si no está jugando
 *   onStop: función() — se llama al hacer clic si está jugando
 *   isPlaying: boolean — ¿este juego es el que se está reproduciendo?
 *
 * El componente NO hace llamadas a la API. Solo renderiza y llama callbacks.
 * Esto es la diferencia principal con Cartucho.jsx de la v1, que hacía fetch dentro.
 */
export default function GameCard({ game, onPlay, onStop, isPlaying }) {
  const handleClick = () => {
    if (isPlaying) {
      onStop();
    } else {
      onPlay(game.nombre, game.consola);
    }
  };

  return (
    <div
      className={`relative w-56 h-[320px] bg-gray-200 rounded-2xl shadow-2xl p-2 border-4
        transition-all duration-300 hover:scale-105 active:scale-95 cursor-pointer
        ${isPlaying ? "border-neon-green shadow-green-500/50" : "border-gray-700 hover:border-neon-cyan"}`}
      onClick={handleClick}
    >
      {/* Pantalla del cartucho — muestra la imagen del juego */}
      <div
        className={`w-40 h-24 mx-auto rounded-lg border-2 border-gray-800 shadow-inner mb-2 overflow-hidden
          ${isPlaying ? "ring-2 ring-neon-green" : ""}`}
      >
        <img
          src={`/assets/videojuegos/${game.imagen}`}
          alt={game.nombre}
          className="w-full h-full object-cover"
          onError={(e) => { e.target.src = "/assets/videojuegos/default.jpg"; }}
        />
      </div>

      {/* Cruceta decorativa (puro CSS, no funcional) */}
      <div className="absolute left-4 bottom-16">
        <div className="flex flex-col items-center">
          <div className="w-6 h-2 bg-black rounded" />
          <div className="flex">
            <div className="w-2 h-6 bg-black rounded" />
            <div className="w-2 h-0" />
            <div className="w-2 h-6 bg-black rounded" />
          </div>
          <div className="w-6 h-2 bg-black rounded" />
        </div>
      </div>

      {/* LED de encendido — verde si está jugando, rojo si no */}
      <div className="absolute bottom-14 left-1/2 -translate-x-1/2">
        <div
          className={`w-10 h-10 rounded-full border-4 shadow-lg transition-colors
            ${isPlaying
              ? "bg-green-500 border-green-700 shadow-green-500/50"
              : "bg-red-500 border-red-700 shadow-red-500/50"
            }`}
        />
      </div>

      {/* Botones A/B decorativos */}
      <div className="absolute right-4 bottom-12 flex flex-col gap-2">
        <div className="bg-red-600 w-5 h-5 rounded-full shadow-lg" />
        <div className="bg-red-600 w-5 h-5 rounded-full shadow-lg" />
      </div>

      {/* Nombre del juego */}
      <div className="absolute bottom-2 left-1/2 -translate-x-1/2 text-xs font-bold text-gray-800 font-arcade text-center w-full px-2 truncate">
        {game.nombre.toUpperCase()}
      </div>

      {/* Badge PLAYING animado */}
      {isPlaying && (
        <div className="absolute top-2 right-2 bg-neon-green text-black text-[10px] font-arcade px-2 py-1 rounded animate-pulse-neon">
          PLAYING
        </div>
      )}
    </div>
  );
}
```

### `frontend/src/components/films/FilmCard.jsx`

```jsx
import React from "react";

/**
 * Tarjeta de película con estética de cinta VHS/bobina.
 *
 * Mismo patrón que GameCard: no hace llamadas a la API.
 * Recibe callbacks onPlay/onStop del padre.
 */
export default function FilmCard({ film, onPlay, onStop, isPlaying }) {
  const handleClick = () => {
    if (isPlaying) {
      onStop();
    } else {
      onPlay(film.nombre);
    }
  };

  return (
    <div
      onClick={handleClick}
      className={`relative bg-black border-4 rounded-lg w-64 h-40 shadow-lg
        transition-all duration-300 cursor-pointer hover:scale-105 active:scale-95
        ${isPlaying
          ? "border-neon-green shadow-green-500/50"
          : "border-gray-700 hover:border-neon-red shadow-red-500/30"
        }`}
    >
      {/* Bobinas de cinta decorativas */}
      <div className="absolute top-[20%] left-4 w-14 h-14 bg-gray-600 rounded-full border-2 border-gray-800 opacity-50" />
      <div className="absolute top-[20%] right-4 w-14 h-14 bg-gray-600 rounded-full border-2 border-gray-800 opacity-50" />

      {/* Imagen de la película (centrada sobre las bobinas) */}
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <img
          src={`/assets/peliculas/${film.imagen}`}
          alt={film.nombre}
          className="w-28 h-24 object-cover rounded-md shadow-inner"
          onError={(e) => { e.target.src = "/assets/peliculas/default.jpg"; }}
        />
      </div>

      {/* Nombre o estado */}
      <div className="absolute bottom-1 left-1 right-1 z-20">
        <div className="px-2 py-1 bg-black/80 rounded text-center">
          {isPlaying ? (
            <span className="text-neon-green text-xs font-arcade animate-pulse-neon">
              Reproduciendo
            </span>
          ) : (
            <span className="text-white text-xs font-bold truncate block">
              {film.nombre.toUpperCase()}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
```

## 5.9 Páginas

### `frontend/src/pages/Home.jsx`

```jsx
import React, { useState, useEffect, useRef } from "react";
import Layout from "../components/layout/Layout";
import { usePlayback } from "../hooks/usePlayback";

/**
 * Página de inicio. Muestra:
 * - Botón para reproducir música de fondo
 * - Cartel de neón con la descripción del proyecto
 * - Estado actual de reproducción (si hay algo en marcha)
 */
export default function Home() {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef(null);        // useRef para mantener la referencia al audio entre renders
  const { current, fetchCurrent } = usePlayback();

  useEffect(() => {
    // Crear el objeto Audio al montar el componente
    audioRef.current = new Audio("/assets/musica/sonic.mp3");
    audioRef.current.loop = true;    // Reproducir en bucle
    fetchCurrent();                  // Comprobar si hay algo reproduciéndose

    // Cleanup: parar audio al desmontar (cambiar de página)
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, [fetchCurrent]);

  const toggleMusic = () => {
    if (!audioRef.current) return;
    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play().catch(() => {});
      // catch vacío: los navegadores bloquean autoplay sin interacción.
      // Si falla, simplemente no suena (no es un error crítico).
    }
    setIsPlaying(!isPlaying);
  };

  return (
    <Layout backgroundImage="/assets/fondo/arcade.png">
      <div className="flex flex-col items-center justify-center min-h-[80vh]">
        {/* Botón música */}
        <button
          onClick={toggleMusic}
          className={`px-6 py-3 rounded-md border-2 font-arcade text-sm transition-all duration-300 mb-8
            ${isPlaying
              ? "border-neon-yellow text-neon-yellow hover:bg-neon-yellow hover:text-black"
              : "border-neon-cyan text-neon-cyan hover:bg-neon-cyan hover:text-black"
            }`}
        >
          {isPlaying ? "Parar Musica" : "Reproducir Musica"}
        </button>

        {/* Cartel principal */}
        <div className="w-11/12 sm:w-8/12 md:w-6/12 lg:w-4/12 p-6 rounded-lg bg-black/80 text-center shadow-xl border-2 border-neon-yellow">
          <h2 className="text-3xl md:text-4xl font-extrabold mb-4 text-neon-yellow font-orbitron neon-text-yellow">
            ArcadiaX
          </h2>
          <p className="text-sm md:text-base text-neon-cyan leading-relaxed font-orbitron">
            Explora el mundo de los juegos clasicos con nuestra recreativa casera.
            Vive la nostalgia de los 80 con una seleccion de consolas retro,
            musica y un ambiente arcade.
          </p>
          <p className="mt-4 text-sm md:text-base text-neon-yellow font-bold font-orbitron">
            Preparate para revivir la magia!
          </p>
        </div>

        {/* Indicador de estado actual */}
        {current.type !== "none" && (
          <div className="mt-8 px-6 py-3 bg-black/80 border-2 border-neon-green rounded-lg animate-pulse-neon">
            <p className="text-neon-green font-arcade text-xs text-center">
              Ahora: {current.data?.nombre || "Reproduciendo..."}
            </p>
          </div>
        )}
      </div>
    </Layout>
  );
}
```

### `frontend/src/pages/Consoles.jsx`

```jsx
import React from "react";
import Layout from "../components/layout/Layout";
import Loading from "../components/layout/Loading";
import ErrorMessage from "../components/layout/ErrorMessage";
import ConsoleCard from "../components/videogames/ConsoleCard";
import { useConsoles } from "../hooks/useVideogames";

/**
 * Página de selección de consola.
 * Muestra una cuadrícula de tarjetas, cada una es una consola disponible.
 * Al hacer clic en una, navega a /juegos/{consola}.
 */
export default function Consoles() {
  const { consoles, loading, error } = useConsoles();

  return (
    <Layout backgroundImage="/assets/fondo/arcade.jpg">
      <div className="flex flex-col items-center min-h-[80vh]">
        <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-center mb-8 uppercase tracking-wide font-orbitron neon-text-red">
          Elige tu consola
        </h2>

        {loading && <Loading text="Cargando consolas..." />}
        {error && <ErrorMessage message={error} />}

        {!loading && !error && (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6 max-w-6xl mx-auto justify-items-center">
            {consoles.length > 0 ? (
              consoles.map((consola) => (
                <ConsoleCard key={consola} consola={consola} />
              ))
            ) : (
              <p className="text-white text-sm col-span-full text-center font-arcade">
                No hay consolas disponibles
              </p>
            )}
          </div>
        )}
      </div>
    </Layout>
  );
}
```

### `frontend/src/pages/Games.jsx`

```jsx
import React from "react";
import { useParams } from "react-router-dom";
import Layout from "../components/layout/Layout";
import Loading from "../components/layout/Loading";
import ErrorMessage from "../components/layout/ErrorMessage";
import GameCard from "../components/videogames/GameCard";
import { useVideogames } from "../hooks/useVideogames";
import { usePlayback } from "../hooks/usePlayback";

/**
 * Página de juegos de una consola.
 *
 * useParams() extrae {consolaNombre} de la URL /juegos/:consolaNombre
 * useVideogames(consolaNombre) carga los juegos de esa consola
 * usePlayback() gestiona la reproducción (play/stop)
 *
 * El flujo cuando haces clic en un juego:
 * 1. GameCard llama onPlay(nombre, consola)
 * 2. handlePlay llama playGame del hook
 * 3. El hook llama playbackService.playGame (HTTP al backend)
 * 4. El backend publica evento Redis
 * 5. El arcade engine lo recibe y abre el emulador
 * 6. El hook llama refresh() para actualizar los datos sin recargar página
 */
export default function Games() {
  const { consolaNombre } = useParams();
  const { games, loading, error, refresh } = useVideogames(consolaNombre);
  const { current, playGame, stop, loading: playbackLoading, error: playbackError, clearError } = usePlayback();

  const handlePlay = async (nombre, consola) => {
    await playGame(nombre, consola);
    refresh();     // Actualiza la lista de juegos (para reflejar play=true)
  };

  const handleStop = async () => {
    await stop();
    refresh();     // Actualiza la lista (para reflejar play=false)
  };

  return (
    <Layout backgroundImage="/assets/fondo/comecocos.jpg">
      <div className="flex flex-col items-center">
        <div className="text-center mb-8">
          <h1 className="inline-block text-2xl sm:text-4xl font-bold text-neon-yellow font-orbitron neon-text-yellow bg-black px-4 py-2 rounded-lg border-2 border-neon-yellow">
            {consolaNombre?.toUpperCase()}
          </h1>
        </div>

        {/* Error de playback (ej: "ya hay un juego en reproducción") */}
        {playbackError && (
          <div className="mb-4 px-4 py-2 bg-red-900/80 border border-neon-red rounded-md animate-fade-in">
            <p className="text-neon-red text-xs font-arcade">{playbackError}</p>
            <button onClick={clearError} className="text-white text-xs underline mt-1">Cerrar</button>
          </div>
        )}

        {loading && <Loading text="Cargando juegos..." />}
        {error && <ErrorMessage message={error} onRetry={refresh} />}

        {!loading && !error && (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8 max-w-5xl mx-auto justify-items-center">
            {games.length > 0 ? (
              games.map((game) => (
                <GameCard
                  key={game._id}
                  game={game}
                  onPlay={handlePlay}
                  onStop={handleStop}
                  isPlaying={current.type === "game" && current.data?._id === game._id}
                />
              ))
            ) : (
              <p className="text-white text-lg col-span-full text-center font-arcade">
                No hay juegos para esta consola
              </p>
            )}
          </div>
        )}

        {/* Toast de carga en la esquina */}
        {playbackLoading && (
          <div className="fixed bottom-4 right-4 bg-black/90 border-2 border-neon-cyan rounded-lg px-4 py-2 animate-fade-in">
            <p className="text-neon-cyan text-xs font-arcade">Cargando...</p>
          </div>
        )}
      </div>
    </Layout>
  );
}
```

### `frontend/src/pages/Films.jsx`

```jsx
import React, { useEffect } from "react";
import Layout from "../components/layout/Layout";
import Loading from "../components/layout/Loading";
import ErrorMessage from "../components/layout/ErrorMessage";
import FilmCard from "../components/films/FilmCard";
import { useFilms } from "../hooks/useFilms";
import { usePlayback } from "../hooks/usePlayback";

/**
 * Página de películas (Homeflix).
 * Mismo patrón que Games.jsx pero para películas.
 */
export default function Films() {
  const { films, loading, error, refresh } = useFilms();
  const { current, playFilm, stop, fetchCurrent, loading: playbackLoading, error: playbackError, clearError } = usePlayback();

  useEffect(() => {
    fetchCurrent();    // Comprobar si hay algo reproduciéndose al cargar
  }, [fetchCurrent]);

  const handlePlay = async (nombre) => {
    await playFilm(nombre);
    refresh();
  };

  const handleStop = async () => {
    await stop();
    refresh();
  };

  return (
    <Layout backgroundImage="/assets/fondo/tele.jpg">
      <div className="flex flex-col items-center">
        <h1 className="text-3xl sm:text-4xl font-bold text-neon-red font-orbitron neon-text-red mb-8">
          HOMEFLIX
        </h1>

        {playbackError && (
          <div className="mb-4 px-4 py-2 bg-red-900/80 border border-neon-red rounded-md animate-fade-in">
            <p className="text-neon-red text-xs font-arcade">{playbackError}</p>
            <button onClick={clearError} className="text-white text-xs underline mt-1">Cerrar</button>
          </div>
        )}

        {loading && <Loading text="Cargando peliculas..." />}
        {error && <ErrorMessage message={error} onRetry={refresh} />}

        {!loading && !error && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-[1440px] mx-auto justify-items-center">
            {films.length > 0 ? (
              films.map((film) => (
                <FilmCard
                  key={film._id}
                  film={film}
                  onPlay={handlePlay}
                  onStop={handleStop}
                  isPlaying={current.type === "film" && current.data?._id === film._id}
                />
              ))
            ) : (
              <p className="text-white font-arcade text-sm col-span-full text-center">
                No hay peliculas disponibles
              </p>
            )}
          </div>
        )}

        {playbackLoading && (
          <div className="fixed bottom-4 right-4 bg-black/90 border-2 border-neon-cyan rounded-lg px-4 py-2 animate-fade-in">
            <p className="text-neon-cyan text-xs font-arcade">Cargando...</p>
          </div>
        )}
      </div>
    </Layout>
  );
}
```

## 5.10 App y Router — `frontend/src/App.jsx`

```jsx
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Consoles from "./pages/Consoles";
import Games from "./pages/Games";
import Films from "./pages/Films";

/**
 * Componente raíz de la aplicación.
 *
 * BrowserRouter habilita la navegación SPA (Single Page Application).
 * En vez de cargar una página nueva del servidor en cada navegación,
 * React cambia el componente que se renderiza según la URL.
 *
 * Routes:
 *   /               → Home (página de inicio)
 *   /consolas        → Consoles (lista de consolas)
 *   /juegos/:nombre  → Games (juegos de una consola)
 *   /peliculas       → Films (Homeflix)
 */
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/consolas" element={<Consoles />} />
        <Route path="/juegos/:consolaNombre" element={<Games />} />
        <Route path="/peliculas" element={<Films />} />
      </Routes>
    </BrowserRouter>
  );
}
```

---

# PARTE 6: SCRIPT DE MIGRACIÓN

## `scripts/migrate_v1_to_v2.py`

```python
"""
Script de migración: ArcadiaX v1 → v2

Ejecutar UNA SOLA VEZ para copiar los datos de la base de datos
de la versión 1 al nuevo esquema de la versión 2.

Uso:
    python scripts/migrate_v1_to_v2.py

Requisitos:
    - MongoDB corriendo en localhost:27017
    - La BBDD "arcadiax" (v1) debe existir con datos
    - pip install motor
"""
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio


async def migrate():
    client = AsyncIOMotorClient("mongodb://localhost:27017")

    v1 = client["arcadiax"]       # BBDD original (v1)
    v2 = client["arcadiax_v2"]    # BBDD nueva (v2)

    # Migrar videojuegos
    count_games = 0
    async for game in v1["videojuegos"].find():
        await v2["videogames"].insert_one({
            "nombre": game["nombre"],
            "consola": game.get("consola", ""),
            "ubicacion": game.get("ubicacion", ""),
            "trailer": game.get("trailer", ""),
            "imagen": game.get("imagen", ""),
            "play": False,          # Resetear estado
            "abierto": False,
        })
        count_games += 1

    # Migrar películas
    count_films = 0
    async for film in v1["peliculas"].find():
        await v2["films"].insert_one({
            "nombre": film["nombre"],
            "ubicacion": film.get("ubicacion", ""),
            "trailer": film.get("trailer", ""),
            "imagen": film.get("imagen", ""),
            "play": False,
            "abierto": False,
        })
        count_films += 1

    print(f"Migración completada: {count_games} juegos, {count_films} películas")
    client.close()


if __name__ == "__main__":
    asyncio.run(migrate())
```

---

# PARTE 7: RESUMEN

## Todos los archivos del proyecto

```
arcadiax-v2/
├── .env                                    → Variables de entorno
├── .gitignore                              → Archivos ignorados por Git
├── docker-compose.yml                      → Levanta todo con un comando
│
├── shared/
│   ├── events.py                           → Definición de todos los eventos
│   └── logger.py                           → Logger unificado
│
├── backend/
│   ├── main.py                             → Entrypoint FastAPI
│   ├── config.py                           → Lee .env
│   ├── database.py                         → Conexión MongoDB
│   ├── dependencies.py                     → Inyección de dependencias
│   ├── Dockerfile                          → Contenedor del backend
│   ├── requirements.txt                    → Dependencias Python
│   ├── models/
│   │   ├── videogame.py                    → Validación de datos (Pydantic)
│   │   └── film.py
│   ├── repositories/
│   │   ├── base.py                         → CRUD genérico
│   │   ├── videogame_repo.py               → Queries de videojuegos
│   │   └── film_repo.py                    → Queries de películas
│   ├── services/
│   │   ├── videogame_service.py            → Lógica de videojuegos
│   │   ├── film_service.py                 → Lógica de películas
│   │   └── playback_service.py             → Control de reproducción + eventos
│   ├── routes/
│   │   ├── videogames.py                   → Endpoints /videogames
│   │   ├── films.py                        → Endpoints /films
│   │   ├── playback.py                     → Endpoints /playback
│   │   └── health.py                       → GET /health
│   └── events/
│       └── publisher.py                    → Publicar en Redis
│
├── arcade/
│   ├── main.py                             → ArcadeEngine (motor principal)
│   ├── config.py                           → Lee .env
│   ├── requirements.txt                    → Dependencias Python
│   ├── emulators/
│   │   ├── base.py                         → Interfaz EmulatorDriver
│   │   ├── retroarch.py                    → Driver RetroArch (multi-consola)
│   │   ├── ppsspp.py                       → Driver PPSSPP (PSP)
│   │   └── registry.py                     → Mapeo consola → driver
│   ├── playback/
│   │   ├── state_machine.py                → Máquina de estados (6 estados)
│   │   ├── game_controller.py              → Lanza/cierra emuladores
│   │   └── media_controller.py             → Reproduce trailers con mpv/VLC
│   ├── input/
│   │   └── arcade_input.py                 → Lee botones/joystick del arcade
│   └── events/
│       ├── publisher.py                    → Publicar en Redis
│       └── listener.py                     → Escuchar eventos de Redis
│
├── frontend/
│   ├── package.json                        → Dependencias npm
│   ├── tailwind.config.js                  → Tema visual (colores neón, fuentes)
│   ├── Dockerfile                          → Contenedor del frontend
│   ├── nginx.conf                          → Servidor web para producción
│   ├── public/
│   │   └── index.html                      → HTML base
│   └── src/
│       ├── index.js                        → Entrypoint React
│       ├── index.css                       → Estilos globales + efectos neón
│       ├── App.jsx                         → Router (4 rutas)
│       ├── config/
│       │   └── api.js                      → Instancia axios centralizada
│       ├── services/
│       │   ├── videogameService.js          → Llamadas /videogames
│       │   ├── filmService.js               → Llamadas /films
│       │   └── playbackService.js           → Llamadas /playback
│       ├── hooks/
│       │   ├── useVideogames.js             → Hook: cargar juegos/consolas
│       │   ├── useFilms.js                  → Hook: cargar películas
│       │   └── usePlayback.js               → Hook: controlar reproducción
│       ├── components/
│       │   ├── layout/
│       │   │   ├── Navbar.jsx               → Barra de navegación
│       │   │   ├── Layout.jsx               → Wrapper con fondo + navbar
│       │   │   ├── Loading.jsx              → Spinner de carga
│       │   │   └── ErrorMessage.jsx         → Mensaje de error + reintentar
│       │   ├── videogames/
│       │   │   ├── ConsoleCard.jsx          → Tarjeta de consola
│       │   │   └── GameCard.jsx             → Tarjeta de juego (cartucho)
│       │   └── films/
│       │       └── FilmCard.jsx             → Tarjeta de película (VHS)
│       └── pages/
│           ├── Home.jsx                     → Página inicio
│           ├── Consoles.jsx                 → Selección de consola
│           ├── Games.jsx                    → Juegos de una consola
│           └── Films.jsx                    → Homeflix (películas)
│
└── scripts/
    └── migrate_v1_to_v2.py                 → Migración de datos v1 → v2
```
