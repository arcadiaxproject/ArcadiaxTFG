from abc import ABC, abstractmethod


class EmulatorDriver(ABC):
    """
    Interfaz base que todo driver de emulador debe implementar.
    Garantiza que todos los emuladores se usan de la misma forma:

        driver = get_driver("ps1")
        await driver.launch("/roms/crash.bin")
        if await driver.is_running():
            await driver.save_state()
        await driver.terminate()
    """

    @abstractmethod
    async def launch(self, rom_path: str) -> bool:
        """Lanza el emulador con una ROM. Devuelve True si arranco bien."""
        pass

    @abstractmethod
    async def is_running(self) -> bool:
        """El emulador sigue ejecutandose?"""
        pass

    @abstractmethod
    async def terminate(self):
        """Cierra el emulador."""
        pass

    @abstractmethod
    async def save_state(self):
        """Guarda el estado de la partida."""
        pass

    @abstractmethod
    async def load_state(self):
        """Carga el ultimo estado guardado."""
        pass
