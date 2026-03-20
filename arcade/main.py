import asyncio
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from arcade.playback.state_machine import ArcadeStateMachine, State
from arcade.playback.game_controller import GameController
from arcade.playback.media_controller import MediaController
from arcade.input.arcade_input import ArcadeInputReader
from arcade.events.listener import EventListener
from arcade.events.publisher import EventPublisher
from shared.events import Events
from arcade.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("arcadiax")


class ArcadeEngine:
    """
    Motor principal del arcade. Orquesta todo:
    - Escucha eventos Redis (del backend y del input fisico)
    - Gestiona la maquina de estados
    - Controla emuladores y reproductor de trailers
    - Monitoriza que todo siga corriendo

    Ejecuta 3 tareas en paralelo:
    1. EventListener  -> escucha eventos Redis
    2. ArcadeInput    -> lee botones del arcade fisico
    3. monitor_loop   -> comprobacion cada segundo
    """

    def __init__(self):
        self.sm = ArcadeStateMachine()
        self.events = EventPublisher(settings.REDIS_URL)
        self.game = GameController()
        self.media = MediaController(settings.TRAILERS_PATH, settings.MEDIA_PLAYER)
        self.arcade_input = ArcadeInputReader(self.events)
        self.selecting_timer = None

    async def start(self):
        log.info("ArcadiaX Engine v2 iniciado")

        handlers = {
            Events.ARCADE_BUTTON_SELECT: self.on_select,
            Events.WEB_SELECT_REQUEST:   self.on_select,
            Events.GAME_PLAY:            self.on_game_chosen,
            Events.FILM_PLAY:            self.on_film_chosen,
            Events.ARCADE_BUTTON_BACK:   self.on_back,
            Events.PLAYBACK_STOP:        self.on_stop,
        }
        listener = EventListener(handlers, settings.REDIS_URL)

        await asyncio.gather(
            listener.listen(),
            self.arcade_input.start(),
            self.monitor_loop(),
        )

    # ── HANDLERS ────────────────────────────────────────────

    async def on_select(self, data: dict):
        """Alguien quiere seleccionar un juego (boton arcade o acceso web)."""
        if self.sm.state in (State.IDLE, State.TRAILER):
            await self.media.stop()
            self.sm.transition(State.SELECTING)
            await self.events.publish(Events.STATE_CHANGED, {"state": "selecting"})
            self.selecting_timer = asyncio.create_task(self._selecting_timeout(60))

    async def on_game_chosen(self, data: dict):
        """Usuario eligio un juego. Lanzar el emulador."""
        if not self.sm.transition(State.LOADING):
            return
        if self.selecting_timer:
            self.selecting_timer.cancel()

        success = await self.game.launch(data["consola"], data["ubicacion"])
        if success:
            self.sm.transition(State.PLAYING)
            await self.events.publish(Events.STATE_CHANGED, {"state": "playing", "data": data})
        else:
            self.sm.transition(State.IDLE)
            await self.events.publish(Events.STATE_CHANGED, {"state": "idle", "error": "fallo al lanzar"})

    async def on_film_chosen(self, data: dict):
        """Usuario eligio una pelicula. Abrirla con mpv/VLC."""
        if not self.sm.transition(State.LOADING):
            return
        if self.selecting_timer:
            self.selecting_timer.cancel()

        await self.media.play_url(data["ubicacion"])
        self.sm.transition(State.PLAYING)
        await self.events.publish(Events.STATE_CHANGED, {"state": "playing", "data": data})

    async def on_back(self, data: dict):
        """Boton back: cancela seleccion o cierra el emulador segun el estado."""
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
        """Parar todo (viene del backend via POST /playback/stop)."""
        await self.game.terminate()
        await self.media.stop()
        self.sm.transition(State.IDLE)

    # ── MONITOR ─────────────────────────────────────────────

    async def monitor_loop(self):
        """
        Se ejecuta cada segundo:
        - IDLE 30s sin actividad -> poner trailers
        - TRAILER: si el trailer termino -> poner otro
        - PLAYING: si el emulador se cerro -> volver a IDLE
        - PLAYING cada 30s -> auto-guardado
        """
        idle_count = 0
        save_count = 0

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
                if not await self.media.is_playing():
                    await self.media.play_random_trailer()

            elif state == State.PLAYING:
                idle_count = 0
                save_count += 1

                if not await self.game.is_running() and not await self.media.is_playing():
                    log.info("Reproduccion terminada, volviendo a IDLE")
                    self.sm.transition(State.IDLE)
                    await self.events.publish(Events.STATE_CHANGED, {"state": "idle"})
                    save_count = 0

                elif save_count >= 30 and await self.game.is_running():
                    self.sm.transition(State.SAVING)
                    await self.game.save_state()
                    self.sm.transition(State.PLAYING)
                    save_count = 0
            else:
                idle_count = 0

            await asyncio.sleep(1)

    async def _selecting_timeout(self, seconds: int):
        """Si no elige juego en X segundos, volver a IDLE."""
        await asyncio.sleep(seconds)
        if self.sm.is_selecting:
            log.info("Timeout de seleccion")
            self.sm.transition(State.IDLE)
            await self.events.publish(Events.STATE_CHANGED, {"state": "idle"})


if __name__ == "__main__":
    engine = ArcadeEngine()
    asyncio.run(engine.start())
