import asyncio
import shutil
from arcade.emulators.base import EmulatorDriver


class PPSSPPDriver(EmulatorDriver):
    """
    Driver especifico para PPSSPP (emulador de PSP).
    Necesita su propio driver porque no se integra bien con RetroArch.
    """

    def __init__(self, consola: str, ppsspp_path: str = None, **kwargs):
        self.ppsspp_path = ppsspp_path or shutil.which("ppsspp") or shutil.which("PPSSPP")
        self.process = None

    async def launch(self, rom_path: str) -> bool:
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
        # PPSSPP: usar su API HTTP o simular tecla F2
        pass

    async def load_state(self):
        pass
