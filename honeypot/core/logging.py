import logging
from logging.handlers import RotatingFileHandler

FORMAT = logging.Formatter('%(asctime)s %(message)s')

def init_logger(name, file_path):
    # Funnel logger - Capture usernames, passwords and ip addresses
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Initialize and Add handler - Specifies file and formatting
    handler = RotatingFileHandler(file_path, maxBytes=2000, backupCount=5)
    handler.setFormatter(FORMAT)
    logger.addHandler(handler)

    return logger
    