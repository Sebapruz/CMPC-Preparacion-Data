import logging
import os
from config import LOGS_DIR

def get_logger(name):
    """
    Crea un 'vigilante' (logger) que escribe en disco y en pantalla.
    Args:
        name (Str): El nombre del proceso que está hablando (ej: ETL_USUARIOS).
    """
    # 1. Configurar el logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Evitar duplicar mensajes si se llama muchas veces
    if logger.hasHandlers():
        return logger
    
    # 2. Formato: [FECHA] - [PROCESO] - [NIVEL] - [MENSAJE]
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 3. Handler de ARCHIVO (Guarda el historial)
    log_file = os.path.join(LOGS_DIR, "pipeline.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 4. Handler de CONSOLA (Para ver en vivo)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger