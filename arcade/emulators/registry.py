from arcade.emulators.retroarch import RetroArchDriver
from arcade.emulators.ppsspp import PPSSPPDriver
from arcade.emulators.base import EmulatorDriver

# Para añadir una consola nueva, solo hay que añadir una linea aqui
EMULATOR_MAP = {
    "snes":      RetroArchDriver,
    "nes":       RetroArchDriver,
    "gba":       RetroArchDriver,
    "megadrive": RetroArchDriver,
    "n64":       RetroArchDriver,
    "ps1":       RetroArchDriver,
    "arcade":    RetroArchDriver,
    "psp":       PPSSPPDriver,
}


def get_driver(consola: str, **kwargs) -> EmulatorDriver:
    """
    Devuelve el driver correcto para una consola.

        driver = get_driver("ps1")   # -> RetroArchDriver
        driver = get_driver("psp")   # -> PPSSPPDriver
    """
    driver_class = EMULATOR_MAP.get(consola.lower())
    if not driver_class:
        raise ValueError(f"No hay driver para la consola: {consola}")
    return driver_class(consola=consola, **kwargs)
