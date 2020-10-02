"""
    Superclass for database implementations
"""
from threading import Lock
import pickle
import os


class SuperDatabase:

    def load_table(self, table_id: str) -> dict:
        pass

    def write_table(self, table_id: str, data: dict) -> bool:
        pass


SERIAL_DB_PATH = os.path.join('database', 'persistence.va')


class SerialDatabase(SuperDatabase):

    _db_path = None
    _db_lock = None

    def __init__(self, db_path: str = SERIAL_DB_PATH):
        self._db_path = db_path
        self._db_lock = Lock()

    def load_table(self, table_id: str) -> dict:
        """ Load a dict from serialized database """
        try:
            result = pickle.load(open(self._db_path, "rb"))[table_id]
        except (FileNotFoundError, KeyError, pickle.UnpicklingError):
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
            except FileNotFoundError:
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
