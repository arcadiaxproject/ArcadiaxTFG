import logging
from arcade.emulators.registry import get_driver
from arcade.emulators.base import EmulatorDriver

log = logging.getLogger("arcadiax.game")


class GameController:
    """
    Abstrae el ciclo de vida de un juego:
    buscar driver -> lanzar emulador -> monitorizar -> cerrar.
    """

    def __init__(self):
        self.current_driver: EmulatorDriver = None

    async def launch(self, consola: str, rom_path: str) -> bool:
        try:
            self.current_driver = get_driver(consola)
            success = await self.current_driver.launch(rom_path)
            if success:
                log.info(f"Juego lanzado: {rom_path} ({consola})")
            else:
                log.error(f"Fallo al lanzar: {rom_path} ({consola})")
            return success
        except ValueError as e:
            log.error(str(e))
            return False

    async def is_running(self) -> bool:
        if not self.current_driver:
            return False
        return await self.current_driver.is_running()

    async def terminate(self):
        if self.current_driver:
            await self.current_driver.terminate()
            log.info("Emulador cerrado")
            self.current_driver = None

    async def save_state(self):
        if self.current_driver:
            await self.current_driver.save_state()
            log.info("Estado guardado")
