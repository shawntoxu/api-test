import logging
from logging.handlers import RotatingFileHandler
import config

LOG = None

def get_logger():
    logging.basicConfig(format = '[%(levelname)s] [%(asctime)s] %(message)s', 
                        level = logging.INFO) 
    handlers = [
        RotatingFileHandler(config.LOG_PATH,
                            mode='a',
                            maxBytes = config.MAX_LOG_SIZE * 1024 * 1024,
                            backupCount = config.MAX_LOG_COUNT),
    ]
    fmt = logging.Formatter('[%(levelname)s] [%(asctime)s] %(message)s')
    logger = logging.getLogger()
    for handler in handlers:
        handler.setFormatter(fmt)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
    return logger

LOG = get_logger()

