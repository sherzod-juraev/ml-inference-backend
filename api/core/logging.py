from aiologger.handlers.files import AsyncTimedRotatingFileHandler, RolloverInterval
from aiologger import Logger
from aiologger.formatters.base import Formatter
from os import makedirs


all_logger = []


def get_logger(name: str, /) -> Logger:
    dir_name = 'logs'
    makedirs(dir_name, exist_ok=True)
    logger = Logger(
        name=name,
        level='INFO'
    )

    file_handler = AsyncTimedRotatingFileHandler(
        filename=f"{dir_name}/{name}.log",
        encoding='utf-8',
        backup_count=100,
        utc=True,
        when=RolloverInterval.DAYS
    )
    file_formatter = Formatter(
        fmt='%(name)s | %(asctime)s.%(msecs)03d | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.formatter = file_formatter
    logger.add_handler(file_handler)
    all_logger.append(logger)
    return logger