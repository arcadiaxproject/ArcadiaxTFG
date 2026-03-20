import asyncio
import os
import random
import logging

log = logging.getLogger("arcadiax.media")


class MediaController:
    """Controla la reproduccion de trailers y peliculas con mpv o VLC."""

    def __init__(self, trailers_path: str, player: str = "mpv"):
        self.trailers_path = os.path.expanduser(trailers_path)
        self.player = player
        self.process = None

    async def play_random_trailer(self):
        """Reproduce un trailer aleatorio de la carpeta de trailers."""
        if not os.path.isdir(self.trailers_path):
            log.warning(f"Directorio de trailers no existe: {self.trailers_path}")
            return

        videos = [
            f for f in os.listdir(self.trailers_path)
            if f.endswith((".mp4", ".mkv", ".avi", ".mov"))
        ]
        if not videos:
            log.warning("No hay trailers disponibles")
            return

        trailer = os.path.join(self.trailers_path, random.choice(videos))
        log.info(f"Reproduciendo trailer: {trailer}")
        await self._launch(trailer)

    async def play_url(self, url: str):
        """Reproduce un video por ruta o URL."""
        log.info(f"Reproduciendo: {url}")
        await self._launch(url)

    async def _launch(self, path: str):
        if self.player == "mpv":
            args = [self.player, "--fs", "--no-terminal", path]
        else:
            args = [self.player, "--fullscreen", path]
        self.process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )

    async def is_playing(self) -> bool:
        return self.process is not None and self.process.returncode is None

    async def stop(self):
        if self.process and self.process.returncode is None:
            self.process.terminate()
            await self.process.wait()
            log.info("Reproductor parado")
            self.process = None
