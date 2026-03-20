from enum import Enum
import logging

log = logging.getLogger("arcadiax.state")


class State(Enum):
    """
    Los 6 estados posibles del arcade.

    IDLE      -> Encendido pero sin actividad
    TRAILER   -> Reproduciendo trailers en bucle
    SELECTING -> Pantalla de seleccion de juego
    LOADING   -> Cargando el emulador
    PLAYING   -> Jugando o viendo pelicula
    SAVING    -> Auto-guardando (vuelve a PLAYING automaticamente)
    """
    IDLE      = "idle"
    TRAILER   = "trailer"
    SELECTING = "selecting"
    LOADING   = "loading"
    PLAYING   = "playing"
    SAVING    = "saving"


class ArcadeStateMachine:
    """
    Controla las transiciones entre estados.
    Solo permite transiciones validas — rechaza cualquier salto ilegal.
    """

    def __init__(self):
        self.state = State.IDLE

        # Mapa de transiciones validas: estado_actual -> [estados_permitidos]
        self._transitions = {
            State.IDLE:      [State.TRAILER, State.SELECTING],
            State.TRAILER:   [State.IDLE, State.SELECTING],
            State.SELECTING: [State.LOADING, State.IDLE],
            State.LOADING:   [State.PLAYING, State.IDLE],
            State.PLAYING:   [State.SAVING, State.IDLE],
            State.SAVING:    [State.PLAYING, State.IDLE],
        }

    def transition(self, new_state: State) -> bool:
        """
        Intenta cambiar de estado. Devuelve True si la transicion es valida.
        """
        if new_state not in self._transitions.get(self.state, []):
            log.warning(f"Transicion invalida: {self.state.value} -> {new_state.value}")
            return False
        log.info(f"Estado: {self.state.value} -> {new_state.value}")
        self.state = new_state
        return True

    @property
    def is_idle(self):
        return self.state == State.IDLE

    @property
    def is_selecting(self):
        return self.state == State.SELECTING

    @property
    def is_playing(self):
        # SAVING cuenta como playing porque el juego sigue corriendo
        return self.state in (State.PLAYING, State.SAVING)
