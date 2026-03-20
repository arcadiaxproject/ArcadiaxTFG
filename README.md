# ArcadiaX v2

Sistema completo de máquina arcade casera con catálogo web, motor de emulación y reproductor de películas. Diseñado para correr en una Raspberry Pi o PC dedicado conectado a una pantalla y controles arcade físicos.

---

## Índice

- [¿Qué es ArcadiaX?](#qué-es-arcadiax)
- [Arquitectura](#arquitectura)
- [Módulos](#módulos)
- [Tecnologías](#tecnologías)
- [Requisitos previos](#requisitos-previos)
- [Instalación y arranque](#instalación-y-arranque)
  - [Con Docker (recomendado)](#con-docker-recomendado)
  - [Sin Docker (desarrollo local)](#sin-docker-desarrollo-local)
- [Variables de entorno](#variables-de-entorno)
- [API REST](#api-rest)
- [Sistema de eventos](#sistema-de-eventos)
- [Máquina de estados del arcade](#máquina-de-estados-del-arcade)
- [Emuladores soportados](#emuladores-soportados)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Tests](#tests)

---

## ¿Qué es ArcadiaX?

ArcadiaX es una plataforma para convertir cualquier PC o Raspberry Pi en una máquina arcade retro completa. Combina tres componentes principales:

- **Catálogo web** (React): interfaz para explorar juegos y películas desde el navegador o una pantalla táctil.
- **Backend API** (FastAPI): gestiona el catálogo de juegos y películas en MongoDB y controla qué se está reproduciendo.
- **Arcade Engine** (Python async): escucha eventos, gestiona el ciclo de vida de los emuladores y el reproductor de vídeo, y lee los botones físicos del mando arcade.

Los tres módulos se comunican en tiempo real mediante **Redis pub/sub** — cuando el usuario pulsa "Jugar" en el frontend, el backend publica un evento en Redis y el arcade engine lo recibe y abre el emulador correspondiente.

---

## Arquitectura

```
┌──────────────────────────────────────────────────────┐
│                    USUARIO                           │
│         (navegador web o pantalla táctil)            │
└─────────────────────┬────────────────────────────────┘
                      │ HTTP
                      ▼
┌─────────────────────────────────────────────────────┐
│              FRONTEND (React + Nginx)               │
│    Catálogo de juegos │ Homeflix │ Estado actual    │
│    puerto 3000        │                             │
└─────────────────────┬───────────────────────────────┘
                      │ HTTP REST
                      ▼
┌─────────────────────────────────────────────────────┐
│              BACKEND (FastAPI)                      │
│   /videogames  /films  /playback  /health           │
│   puerto 8000                                       │
│                                                     │
│   Routes → Services → Repositories → MongoDB       │
└──────────┬──────────────────────────┬───────────────┘
           │ read/write               │ publish events
           ▼                          ▼
┌──────────────────┐      ┌──────────────────────────┐
│   MongoDB        │      │   Redis pub/sub           │
│   (videogames,   │      │   canal: "arcadiax"       │
│    films)        │      └────────────┬─────────────┘
└──────────────────┘                   │ subscribe
                                       ▼
┌─────────────────────────────────────────────────────┐
│              ARCADE ENGINE (asyncio)                │
│                                                     │
│   EventListener ──→ State Machine                   │
│   ArcadeInput   ──→ GameController (emuladores)     │
│   MonitorLoop   ──→ MediaController (trailers/mpvl) │
└─────────────────────────────────────────────────────┘
```

---

## Módulos

### Backend (`/backend`)

API REST construida con **FastAPI** y **Motor** (driver async para MongoDB). Sigue una arquitectura en capas:

```
Routes → Services → Repositories → MongoDB
```

- **Routes**: endpoints HTTP, validación de entrada con Pydantic
- **Services**: lógica de negocio (reglas como "no puede haber dos cosas reproduciéndose a la vez")
- **Repositories**: acceso a datos, queries MongoDB
- **Events**: publica eventos en Redis cuando cambia el estado de reproducción

### Arcade Engine (`/arcade`)

Motor principal que corre en la máquina física. Implementado con `asyncio` para gestionar varias tareas en paralelo:

1. **EventListener**: suscrito al canal Redis, recibe órdenes del backend y del frontend
2. **ArcadeInputReader**: lee botones físicos mediante `pygame` (joystick USB/encoder)
3. **MonitorLoop**: comprueba cada segundo si el emulador sigue corriendo

Incluye una **máquina de estados** que controla el ciclo de vida del sistema (ver sección dedicada).

### Frontend (`/frontend`)

SPA construida con **React 18** y **react-router-dom**. Consume el backend mediante `axios`.

| Ruta | Página | Descripción |
|------|--------|-------------|
| `/` | Home | Estado actual de reproducción |
| `/consolas` | Consoles | Listado de consolas disponibles |
| `/juegos/:consola` | Games | Juegos de una consola específica |
| `/peliculas` | Films (Homeflix) | Catálogo de películas |

### Shared (`/shared`)

Código compartido entre el backend y el arcade engine:

- `events.py`: constantes de todos los eventos del sistema
- `logger.py`: logger unificado con formato `[HH:MM:SS] nombre | NIVEL | mensaje`

---

## Tecnologías

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Backend | FastAPI + Uvicorn | 0.115 / 0.30 |
| Base de datos | MongoDB + Motor (async) | 7 / 3.5 |
| Mensajería | Redis pub/sub | 7 |
| Arcade engine | Python asyncio + pygame | 3.12 |
| Frontend | React + react-router-dom | 18.3 / 6.26 |
| HTTP client | Axios | 1.7 |
| CSS | Tailwind CSS | 3.4 |
| Contenedores | Docker + Docker Compose | — |
| Servidor web | Nginx (frontend prod) | alpine |

---

## Requisitos previos

### Para desarrollo local (sin Docker)

- Python 3.12+
- Node.js 20+
- MongoDB corriendo en `localhost:27017`
- Redis corriendo en `localhost:6379`

### Para producción (con Docker)

- Docker Desktop o Docker Engine + Docker Compose

### Para el arcade engine (hardware)

- RetroArch instalado (emulación de NES, SNES, GBA, Mega Drive, N64, PS1, Arcade)
- PPSSPP instalado (emulación de PSP)
- mpv o VLC instalado (reproducción de trailers y películas)
- ROMs organizadas por carpetas de consola
- Mando arcade USB compatible con pygame (joystick HID estándar)

---

## Instalación y arranque

### Con Docker (recomendado)

**1. Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/ArcadiaxTFG.git
cd ArcadiaxTFG
```

**2. Crear el archivo `.env`**

```bash
cp .env.example .env
# Edita .env con tus valores
```

**3. Levantar todos los servicios**

```bash
docker compose up -d
```

Esto arranca:
- MongoDB en el puerto 27017
- Redis en el puerto 6379
- Backend API en http://localhost:8000
- Frontend en http://localhost:3000

**4. Verificar que todo funciona**

```bash
curl http://localhost:8000/health
# → {"status": "ok", "service": "arcadiax-backend"}
```

**5. Parar los servicios**

```bash
docker compose down
```

---

### Sin Docker (desarrollo local)

#### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

La API estará disponible en http://localhost:8000
Documentación interactiva: http://localhost:8000/docs

#### Frontend

```bash
cd frontend
npm install
npm start
```

La interfaz estará disponible en http://localhost:3000

#### Arcade Engine

```bash
cd arcade
pip install -r requirements.txt  # pygame, redis, pydantic-settings
python main.py
```

> El arcade engine requiere que RetroArch, PPSSPP y mpv/VLC estén instalados y configurados en el `.env`.

---

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto basándote en `.env.example`:

```bash
# ─── Base de datos ───────────────────────────────
MONGO_USER=admin
MONGO_PASSWORD=admin
MONGO_DB=arcadiax

# URI completa (usada por el backend en Docker)
MONGO_URI=mongodb://admin:admin@mongo:27017/arcadiax?authSource=admin

# Para desarrollo local sin Docker:
# MONGO_URI=mongodb://localhost:27017

# ─── Redis ───────────────────────────────────────
REDIS_URL=redis://localhost:6379

# ─── Backend ─────────────────────────────────────
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# ─── Frontend ────────────────────────────────────
REACT_APP_API_URL=http://localhost:8000

# ─── Arcade Engine ───────────────────────────────
RETROARCH_PATH=/usr/bin/retroarch
PPSSPP_PATH=/usr/bin/ppsspp
ROMS_PATH=/home/usuario/roms
TRAILERS_PATH=/home/usuario/trailers
MEDIA_PLAYER=mpv          # o vlc

# ─── Rutas de medios (Docker) ────────────────────
FILMS_PATH=/ruta/a/tus/peliculas
```

---

## API REST

La documentación interactiva completa está disponible en **http://localhost:8000/docs** cuando el backend está corriendo.

### Videojuegos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/videogames/` | Todos los videojuegos |
| `GET` | `/videogames/consoles` | Lista de consolas disponibles |
| `GET` | `/videogames/console/{consola}` | Juegos de una consola específica |
| `GET` | `/videogames/{id}` | Un juego por su ID |
| `POST` | `/videogames/` | Crear un videojuego nuevo |
| `PUT` | `/videogames/{id}` | Actualizar un videojuego |
| `DELETE` | `/videogames/{id}` | Eliminar un videojuego |

**Ejemplo — crear un juego:**
```bash
curl -X POST http://localhost:8000/videogames/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Crash Bandicoot", "consola": "ps1", "ubicacion": "/roms/ps1/crash.bin"}'
```

**Ejemplo — juegos de una consola:**
```bash
curl http://localhost:8000/videogames/console/snes
```

### Películas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/films/` | Todas las películas |
| `GET` | `/films/{id}` | Una película por su ID |
| `POST` | `/films/` | Crear una película |
| `DELETE` | `/films/{id}` | Eliminar una película |

**Ejemplo — crear una película:**
```bash
curl -X POST http://localhost:8000/films/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Inception", "ubicacion": "/films/inception.mkv"}'
```

### Reproducción

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/playback/game/{nombre}/{consola}` | Iniciar un juego |
| `POST` | `/playback/film/{nombre}` | Iniciar una película |
| `POST` | `/playback/stop` | Parar la reproducción actual |
| `GET` | `/playback/current` | Estado de reproducción actual |
| `GET` | `/playback/trailer` | Obtener un trailer aleatorio |

**Ejemplo — iniciar un juego:**
```bash
curl -X POST http://localhost:8000/playback/game/CrashBandicoot/ps1
```

**Ejemplo — consultar estado actual:**
```bash
curl http://localhost:8000/playback/current
# → {"type": "game", "data": {"nombre": "Crash Bandicoot", "consola": "ps1", ...}}
# → {"type": "film", "data": {"nombre": "Inception", ...}}
# → {"type": "none", "data": null}
```

> **Regla de exclusividad**: solo puede haber una cosa reproduciéndose a la vez. Intentar reproducir algo cuando ya hay algo activo devuelve `400 Bad Request`.

### Health Check

```bash
curl http://localhost:8000/health
# → {"status": "ok", "service": "arcadiax-backend"}
```

---

## Sistema de eventos

Los tres módulos se comunican mediante **Redis pub/sub** en el canal `arcadiax`. Todos los mensajes siguen el formato:

```json
{
  "event": "nombre.del.evento",
  "data": { ... }
}
```

### Eventos disponibles

| Evento | Emisor | Descripción | Payload |
|--------|--------|-------------|---------|
| `input.arcade.select` | Arcade | Botón SELECT pulsado | `{}` |
| `input.arcade.back` | Arcade | Botón BACK pulsado | `{}` |
| `input.arcade.confirm` | Arcade | Botón CONFIRM pulsado | `{}` |
| `input.web.select` | Frontend | Selección desde web | `{nombre, consola}` |
| `state.changed` | Arcade | Cambio de estado | `{state}` |
| `playback.game.play` | Backend | Iniciar juego | `{nombre, consola, ubicacion}` |
| `playback.game.opened` | Arcade | Emulador lanzado | `{nombre}` |
| `playback.game.closed` | Arcade | Emulador cerrado | `{nombre}` |
| `playback.film.play` | Backend | Iniciar película | `{nombre, ubicacion}` |
| `playback.stop` | Backend | Parar todo | `{}` |
| `system.idle` | Arcade | Sin actividad | `{}` |
| `system.shutdown` | Sistema | Apagado | `{}` |

---

## Máquina de estados del arcade

El arcade engine implementa una máquina de estados que controla en qué modo se encuentra el sistema en cada momento:

```
                    ┌─────────┐
               ┌───▶│  IDLE   │◀──────────────────┐
               │    └────┬────┘                    │
               │         │                         │
               │    ┌────▼────┐                    │
               │    │ TRAILER │                    │
               │    └────┬────┘                    │
               │         │                         │
               │    ┌────▼──────┐                  │
               │    │ SELECTING │──────────────────┤
               │    └────┬──────┘                  │
               │         │                         │
               │    ┌────▼────┐                    │
               │    │ LOADING │──────────────────  │
               │    └────┬────┘                    │
               │         │                         │
               │    ┌────▼────┐    ┌─────────┐     │
               └────│ PLAYING │◀──▶│ SAVING  │     │
                    └─────────┘    └────┬────┘     │
                         │              │           │
                         └──────────────┴───────────┘
```

| Estado | Descripción |
|--------|-------------|
| `IDLE` | Sistema encendido, sin actividad |
| `TRAILER` | Reproduciendo trailers en bucle automático |
| `SELECTING` | Usuario navegando por el catálogo |
| `LOADING` | Emulador cargando la ROM |
| `PLAYING` | Juego o película en curso |
| `SAVING` | Guardado automático (vuelve a PLAYING) |

Las transiciones inválidas se ignoran con un log de advertencia — el sistema nunca queda en un estado inconsistente.

---

## Emuladores soportados

| Consola | Emulador | Núcleo RetroArch |
|---------|----------|-----------------|
| NES | RetroArch | FCEUmm |
| SNES | RetroArch | Snes9x |
| Game Boy Advance | RetroArch | mGBA |
| Mega Drive / Genesis | RetroArch | Genesis Plus GX |
| Nintendo 64 | RetroArch | Mupen64Plus-Next |
| PlayStation 1 | RetroArch | Beetle PSX |
| Arcade (MAME) | RetroArch | MAME |
| PSP | PPSSPP | — (nativo) |

Los drivers de emuladores implementan una interfaz común (`EmulatorDriver`) con los métodos `launch`, `is_running`, `terminate`, `save_state` y `load_state`. Añadir soporte para una nueva consola consiste en crear un nuevo driver y registrarlo en `arcade/emulators/registry.py`.

---

## Estructura del proyecto

```
ArcadiaxTFG/
│
├── .env.example                # Plantilla de variables de entorno
├── .gitignore
├── docker-compose.yml          # Orquestación completa con Docker
├── README.md
│
├── shared/                     # Código compartido (backend + arcade)
│   ├── events.py               # Constantes de todos los eventos
│   └── logger.py               # Logger unificado
│
├── backend/                    # API REST (FastAPI)
│   ├── main.py                 # Entrypoint
│   ├── config.py               # Configuración (pydantic-settings)
│   ├── database.py             # Conexión MongoDB async
│   ├── dependencies.py         # Inyección de dependencias
│   ├── requirements.txt
│   ├── Dockerfile
│   │
│   ├── models/                 # Esquemas Pydantic
│   │   ├── Videogame.py        # VideogameCreate, Update, Response
│   │   └── film.py             # FilmCreate, Update, Response
│   │
│   ├── repositories/           # Acceso a datos (MongoDB)
│   │   ├── base.py             # CRUD genérico
│   │   ├── videogame_repo.py   # Queries específicas de juegos
│   │   └── film_repo.py        # Queries específicas de películas
│   │
│   ├── services/               # Lógica de negocio
│   │   ├── videogame_service.py
│   │   ├── film_service.py
│   │   └── playback_service.py # Control de reproducción + eventos Redis
│   │
│   ├── routes/                 # Endpoints HTTP
│   │   ├── videogames.py
│   │   ├── films.py
│   │   └── playback.py
│   │
│   ├── events/
│   │   └── publisher.py        # Publica eventos en Redis
│   │
│   ├── test_base_repo.py       # Tests CRUD contra MongoDB real
│   ├── test_playback.py        # Tests del servicio de reproducción
│   └── test_e2e.py             # Tests end-to-end de la API completa
│
├── arcade/                     # Motor arcade (asyncio)
│   ├── main.py                 # ArcadeEngine — orquesta todo
│   ├── config.py               # Rutas a emuladores y contenido
│   ├── test_state_machine.py
│   │
│   ├── playback/
│   │   ├── state_machine.py    # 6 estados con transiciones válidas
│   │   ├── game_controller.py  # Ciclo de vida del emulador
│   │   └── media_controller.py # Reproducción de trailers/películas
│   │
│   ├── emulators/
│   │   ├── base.py             # Interfaz abstracta EmulatorDriver
│   │   ├── retroarch.py        # Driver para RetroArch
│   │   ├── ppsspp.py           # Driver para PPSSPP (PSP)
│   │   └── registry.py         # Mapa consola → driver
│   │
│   ├── events/
│   │   ├── publisher.py        # Publica en Redis
│   │   └── listener.py         # Suscripción al canal arcadiax
│   │
│   └── input/
│       └── arcade_input.py     # Lectura de botones físicos (pygame)
│
└── frontend/                   # Interfaz web (React)
    ├── package.json
    ├── Dockerfile              # Build multi-etapa Node → Nginx
    ├── nginx.conf              # Configuración SPA routing
    ├── tailwind.config.js
    ├── postcss.config.js
    │
    ├── public/
    │   └── index.html
    │
    └── src/
        ├── App.jsx             # Router principal
        ├── index.js
        ├── index.css
        │
        ├── config/
        │   └── api.js          # Instancia axios centralizada
        │
        ├── services/           # Llamadas al backend
        │   ├── videogameService.js
        │   ├── filmService.js
        │   └── playbackService.js
        │
        ├── hooks/              # Lógica React reutilizable
        │   ├── useVideogames.js
        │   ├── useFilms.js
        │   └── usePlayback.js
        │
        ├── components/
        │   ├── layout/
        │   │   ├── Layout.jsx
        │   │   ├── Navbar.jsx
        │   │   ├── Loading.jsx
        │   │   └── ErrorMessage.jsx
        │   ├── videogames/
        │   │   ├── ConsoleCard.jsx
        │   │   └── GameCard.jsx
        │   └── films/
        │       └── FilmCard.jsx
        │
        └── pages/
            ├── Home.jsx
            ├── Consoles.jsx
            ├── Games.jsx
            └── Films.jsx
```

---

## Tests

### Tests del repositorio base

Prueba los 5 métodos CRUD contra MongoDB real:

```bash
cd backend
python test_base_repo.py
```

### Tests del servicio de reproducción

Prueba play_game, play_film, stop, conflictos y verifica eventos Redis:

```bash
cd backend
python test_playback.py
```

### Tests end-to-end de la API

Prueba todos los endpoints HTTP en secuencia. Crea y limpia sus propios datos de prueba:

```bash
cd backend
python test_e2e.py
```

### Tests de la máquina de estados

Prueba transiciones válidas e inválidas del arcade engine:

```bash
cd arcade
python test_state_machine.py
```

---

## Licencia

Proyecto de Trabajo de Fin de Grado. Uso académico.
