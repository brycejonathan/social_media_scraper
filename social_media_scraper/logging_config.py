# logging_config.py

import logging
import sys

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    # StreamHandler for console output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # FileHandler for logging to a file (optional)
    # file_handler = logging.FileHandler('app.log')
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)
