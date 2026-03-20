import logging
import sys


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Crea un logger con formato unificado para todo el proyecto.
    Uso:
        from shared.logger import setup_logger
        log = setup_logger("arcadiax.backend")
        log.info("Servidor arrancado")
        # Output: [14:32:05] arcadiax.backend | INFO | Servidor arrancado
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evitar duplicar handlers si se llama varias veces
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            "[%(asctime)s] %(name)s | %(levelname)s | %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
