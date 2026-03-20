import asyncio
import logging

log = logging.getLogger("arcadiax.input")


class ArcadeInputReader:
    """
    Lee los botones del encoder USB de la maquina arcade.
    El encoder se comporta como un joystick — pygame lo detecta y lee sus inputs.
    Cuando se pulsa un boton, publica el evento Redis correspondiente.
    """

    BUTTON_MAP = {
        0: "select",
        1: "back",
        2: "confirm",
    }

    def __init__(self, event_publisher):
        self.events = event_publisher
        self.running = False

    async def start(self):
        try:
            import pygame
            pygame.init()
            pygame.joystick.init()
        except ImportError:
            log.warning("pygame no instalado, input arcade deshabilitado")
            return

        if pygame.joystick.get_count() == 0:
            log.warning("No se detecto joystick/encoder arcade USB")
            while True:
                await asyncio.sleep(10)

        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        log.info(f"Arcade input detectado: {joystick.get_name()}")

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    action = self.BUTTON_MAP.get(event.button)
                    if action:
                        await self._handle_action(action)
                elif event.type == pygame.JOYAXISMOTION:
                    if abs(event.value) > 0.5:
                        await self._handle_action("select")
            await asyncio.sleep(0.05)

    async def _handle_action(self, action: str):
        from shared.events import Events
        log.info(f"Input arcade: {action}")
        event_map = {
            "select":  Events.ARCADE_BUTTON_SELECT,
            "back":    Events.ARCADE_BUTTON_BACK,
            "confirm": Events.ARCADE_BUTTON_CONFIRM,
        }
        event = event_map.get(action)
        if event:
            await self.events.publish(event, {})

    def stop(self):
        self.running = False
