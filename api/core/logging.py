from logging.handlers import RotatingFileHandler
from os import makedirs
import logging


def get_logger(name: str, /) -> logging.Logger:

    makedirs('logs', exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    file_handler: RotatingFileHandler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=5 * 1024 * 1024,
        backupCount=100
    )
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    return logger