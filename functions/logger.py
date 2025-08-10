import logging
from logging.handlers import RotatingFileHandler
import os
from config import LOG_FILE

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Console Handler
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        logger.addHandler(console_handler)

    # File Handler
    if not any(isinstance(handler, RotatingFileHandler) for handler in logger.handlers):
        file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)

    # Opcional: Aqui pode ativar o DEBUG por variável de ambiente
    if os.getenv('AUTORECON_DEBUG') == 'true':
        logger.setLevel(logging.DEBUG)

    return logger


