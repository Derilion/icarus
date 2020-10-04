"""
    Superclass for database implementations
"""
from appdirs import user_data_dir
from threading import Lock
import pickle
import os


class SuperDatabase:

    def load_table(self, table_id: str) -> dict:
        pass

    def write_table(self, table_id: str, data: dict) -> bool:
        pass


SERIAL_DB_PATH = user_data_dir('icarus', 'derilion')
SERIAl_DB_FILE = os.path.join(SERIAL_DB_PATH, 'persistence.va')


class SerialDatabase(SuperDatabase):

    _db_path = None
    _db_lock = None

    def __init__(self, db_path: str = SERIAl_DB_FILE):
        self._db_path = db_path
        self._db_lock = Lock()
        if not os.path.exists(SERIAL_DB_PATH):
            os.makedirs(SERIAL_DB_PATH)

    def load_table(self, table_id: str) -> dict:
        """ Load a dict from serialized database """
        try:
            result = pickle.load(open(self._db_path, "rb"))[table_id]
        except (PermissionError, FileNotFoundError, KeyError, pickle.UnpicklingError):
            # todo: implement logging
            result = dict()
        return result

    def write_table(self, table_id: str, data: dict) -> bool:
        """ Dump a given dict to the database file """

        # ensure thread safe writing to database file
        with self._db_lock:
            # load data from database file if it exists
            try:
                database = pickle.load(open(self._db_path, "rb"))
            except (PermissionError, FileNotFoundError, KeyError, pickle.UnpicklingError):
                database = dict()

            # overwrite existing content
            database[table_id] = data

            # write data to database file
            try:
                pickle.dump(database, open(self._db_path, "wb"))
                return True
            except pickle.PicklingError:
                # todo: implement logging
                return False
