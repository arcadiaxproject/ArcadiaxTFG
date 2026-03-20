import asyncio
import shutil
from arcade.emulators.base import EmulatorDriver


class RetroArchDriver(EmulatorDriver):
    """
    Driver para RetroArch — cubre la mayoria de consolas con un solo programa.
    Cada consola usa un "core" diferente que se pasa con el flag -L.
    """

    CORES = {
        "snes":      "snes9x_libretro",
        "nes":       "nestopia_libretro",
        "gba":       "mgba_libretro",
        "megadrive": "genesis_plus_gx_libretro",
        "n64":       "mupen64plus_next_libretro",
        "ps1":       "pcsx_rearmed_libretro",
        "arcade":    "mame_libretro",
    }

    def __init__(self, consola: str, retroarch_path: str = None, **kwargs):
        self.consola = consola
        self.core = self.CORES.get(consola)
        self.retroarch_path = retroarch_path or shutil.which("retroarch")
        self.process = None

    async def launch(self, rom_path: str) -> bool:
        if not self.core or not self.retroarch_path:
            return False
        self.process = await asyncio.create_subprocess_exec(
            self.retroarch_path, "-L", self.core, rom_path,
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
        # RetroArch soporta save states via su command interface UDP
        pass

    async def load_state(self):
        pass
