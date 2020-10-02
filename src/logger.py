import logging
import os
from logging import getLogger, FileHandler, Formatter

LOG_FORMAT = Formatter("%(asctime)s [%(levelname)s]: %(message)s")
LOG_LEVEL = logging.DEBUG
LOG_FILE = "../logs/icarus.log"

# make sure directory exists
if not os.path.exists(os.path.join('..', 'logs')):
    os.makedirs(os.path.join('..', 'logs'))

logging.basicConfig(format="%(asctime)s [%(levelname)s]: %(message)s", datefmt='%Y/%m/%d %H:%M:%S', level=logging.ERROR)
console_logger = getLogger("console_logger")
console_handler = logging.StreamHandler()
console_logger.addHandler(console_handler)
console_logger.setLevel(LOG_LEVEL)
console_logger.propagate = True

icarus_logger = getLogger("icarus_logger")
icarus_logger.setLevel(LOG_LEVEL)
icarus_file_handler = FileHandler(LOG_FILE)
icarus_file_handler.setLevel(LOG_LEVEL)
icarus_file_handler.setFormatter(LOG_FORMAT)
icarus_logger.addHandler(icarus_file_handler)
icarus_logger.propagate = False



