import logging
import sys
from colorlog import ColoredFormatter

'''
import os

ENV = os.getenv("ENV", "dev")

if ENV == "dev":
    # logging con colores
else:
    # logging normal o JSON
'''
def setup_logging():
    if logging.getLogger().handlers:
        return

    handler = logging.StreamHandler(sys.stdout)

    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

'''
logger.info("Usuario creado correctamente")
logger.warning("Intento de acceso sospechoso")
logger.error("Error conectando con la base de datos")
logger.debug("Datos recibidos: %s", data)

| Nivel    | Cuándo usarlo                    |
| -------- | -------------------------------- |
| DEBUG    | Información técnica detallada    |
| INFO     | Eventos normales del sistema     |
| WARNING  | Algo raro pero no crítico        |
| ERROR    | Fallo que afecta a una operación |
| CRITICAL | El sistema puede caerse          |
'''