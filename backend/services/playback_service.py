import asyncio
from typing import Optional, Dict
from repositories.videogame_repo import VideogameRepository
from repositories.film_repo import FilmRepository
from events.publisher import EventPublisher
from shared.events import Events
import subprocess

class PlaybackService:
    def __init__(self, videogame_repo: VideogameRepository, film_repo: FilmRepository, publisher: EventPublisher):
        self.videogame_repo = videogame_repo
        self.film_repo = film_repo
        self.publisher = publisher

    async def play_game(self, nombre: str, consola: str) -> Dict:
        if await self.videogame_repo.is_any_playing():
            raise Exception("Ya hay un juego reproduciéndose")
        
        game = await self.videogame_repo.set_play(nombre, consola)
        await self.publisher.publish(Events.GAME_PLAY, {"nombre": nombre, "consola": consola, "ubicacion": game["ubicacion"]})
        return game

    async def play_film(self, nombre: str) -> Dict:
        if await self.videogame_repo.is_any_playing():
            raise Exception("Ya hay un juego reproduciéndose")
        
        film = await self.film_repo.set_play(nombre)
        await self.publisher.publish(Events.FILM_PLAY, {"nombre": nombre, "ubicacion": film["ubicacion"]})
        await self.launch_electron_window(film["ubicacion"])
        return film

    async def get_current(self) -> Dict:
        if game := await self.videogame_repo.get_playing():
            return {"type": "game", "data": game}
        
        if film := await self.film_repo.get_playing():
            return {"type": "film", "data": film}
        
        return {"type": "none"}

    async def stop_playback(self) -> None:
        await self.videogame_repo.reset_all()
        await self.film_repo.reset_all()
        await self.publisher.publish(Events.PLAYBACK_STOP, {})

    async def launch_electron_window(self, ubicacion: str) -> None:
        try:
            # Suponemos que el ejecutable de Electron se llama "electron_app" y está en el PATH
            subprocess.Popen(["electron_app", ubicacion])
        except Exception as e:
            print(f"Error al lanzar la ventana Electron: {e}")

### repositories/film_repo.py
