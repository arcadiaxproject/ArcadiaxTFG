import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from repositories.videogame_repo import VideogameRepository
from repositories.film_repo import FilmRepository
from events.publisher import EventPublisher
from shared.events import Events
from fastapi import HTTPException


class PlaybackService:
    """
    Controla que se esta reproduciendo en el sistema.

    Reglas:
    - Solo puede haber UNA cosa reproduciendose a la vez (juego o pelicula)
    - Al iniciar, marca play=True en MongoDB y publica evento en Redis
    - Al parar, resetea todo y publica PLAYBACK_STOP
    """

    def __init__(self, videogame_repo: VideogameRepository,
                 film_repo: FilmRepository, events: EventPublisher):
        self.videogames = videogame_repo
        self.films = film_repo
        self.events = events

    async def play_game(self, nombre: str, consola: str) -> dict:
        """
        Inicia un juego.
        1. Comprueba que no haya nada reproduciendose
        2. Marca play=True en la BBDD
        3. Publica GAME_PLAY en Redis → el arcade abre el emulador
        """
        if await self.videogames.is_any_playing():
            raise HTTPException(400, "Ya hay un juego en reproduccion")
        if await self.films.is_any_playing():
            raise HTTPException(400, "Hay una pelicula en reproduccion")

        game = await self.videogames.set_play(nombre, consola)
        if not game:
            raise HTTPException(404, f"Juego '{nombre}' ({consola}) no encontrado")

        await self.events.publish(Events.GAME_PLAY, {
            "nombre": nombre,
            "consola": consola,
            "ubicacion": game.get("ubicacion", ""),
            "trailer": game.get("trailer", "")
        })
        return game

    async def play_film(self, nombre: str) -> dict:
        """
        Inicia una pelicula.
        Misma logica que play_game pero para peliculas.
        """
        if await self.videogames.is_any_playing():
            raise HTTPException(400, "Hay un juego en reproduccion")
        if await self.films.is_any_playing():
            raise HTTPException(400, "Ya hay una pelicula en reproduccion")

        film = await self.films.set_play(nombre)
        if not film:
            raise HTTPException(404, f"Pelicula '{nombre}' no encontrada")

        await self.events.publish(Events.FILM_PLAY, {
            "nombre": nombre,
            "ubicacion": film.get("ubicacion", "")
        })
        return film

    async def stop(self):
        """
        Para toda la reproduccion.
        Resetea juegos y peliculas en BBDD y publica PLAYBACK_STOP.
        """
        await self.videogames.reset_all()
        await self.films.reset_all()
        await self.events.publish(Events.PLAYBACK_STOP, {})

    async def get_current(self) -> dict:
        """
        Devuelve que se esta reproduciendo ahora.
        {"type": "game", "data": {...}}
        {"type": "film", "data": {...}}
        {"type": "none", "data": null}
        """
        game = await self.videogames.get_playing()
        if game:
            return {"type": "game", "data": game}
        film = await self.films.get_playing()
        if film:
            return {"type": "film", "data": film}
        return {"type": "none", "data": None}

    async def get_random_trailer(self) -> str:
        """Trailer aleatorio — busca primero en juegos, luego en peliculas."""
        trailer = await self.videogames.get_random_trailer()
        if not trailer:
            trailer = await self.films.get_random_trailer()
        if not trailer:
            raise HTTPException(404, "No hay trailers disponibles")
        return trailer
