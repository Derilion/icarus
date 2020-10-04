import logging
import os
from appdirs import user_log_dir
from logging import getLogger, FileHandler, Formatter
from icarus.persistence.configuration import IniConfiguration

DEFAULT_LEVEL = 'ERROR'
LOG_FORMAT = Formatter("%(asctime)s [%(levelname)s]: %(message)s")
LOG_LEVEL = IniConfiguration.get_config('Logging', 'level')
LOG_PATH = user_log_dir('icarus', 'derilion')
LOG_FILE = os.path.join(LOG_PATH, 'icarus.log')

# make sure directory exists
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

logging.basicConfig(format="%(asctime)s [%(levelname)s]: %(message)s", datefmt='%Y/%m/%d %H:%M:%S', level=logging.ERROR)

# create console logger for errors
console_logger = getLogger("console_logger")
console_handler = logging.StreamHandler()
console_logger.addHandler(console_handler)
console_logger.propagate = True

# create file logger
icarus_logger = getLogger("icarus_logger")
icarus_file_handler = FileHandler(LOG_FILE)
icarus_file_handler.setFormatter(LOG_FORMAT)
icarus_logger.addHandler(icarus_file_handler)
icarus_logger.propagate = False

try:
    console_logger.setLevel(DEFAULT_LEVEL)
    icarus_logger.setLevel(LOG_LEVEL)
    icarus_file_handler.setLevel(LOG_LEVEL)
except ValueError:
    console_logger.setLevel(DEFAULT_LEVEL)
    icarus_logger.setLevel(DEFAULT_LEVEL)
    icarus_file_handler.setLevel(DEFAULT_LEVEL)




