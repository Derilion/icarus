from threading import Lock
import pickle

class DataSource:

    def __init__(self):
        pass


class SQLiteDB:
    """
    todo: implement an encapsulated persistence option for plugins
    """

    def register_dataset(self, data: dict):
        """
        Generate a SQLalchemy data class from the data dictionary
        :param data:
        :return:
        """
        pass

    def load_data(self):
        """
        loads data from the database
        :return:
        """
        pass


class SimpleDB:
    """
    a simple persistence without a heavy db implementation
    """
    _db_file = None
    _persistence_dict = None
    _thread_lock = Lock()

    def __init__(self, filepath: str = "persistence.va"):
        self._db_file = filepath
        self._load_file()

    def save_dict(self, module: str, data: dict) -> bool:
        """
        saves a dictionary as a string in a file
        :param module:
        :param data:
        :return:
        """
        with self._thread_lock:
            self._persistence_dict[module] = data
            self._dump_dict()
        return True

    def load_dict(self, module: str) -> dict:
        """
        returns a saved dictionary
        :param module:
        :return:
        """
        result = None
        with self._thread_lock:
            # check if key in saved dict
            if module in self._persistence_dict:
                result = self._persistence_dict[module]
        return result

    def _load_file(self):
        """
        loads the old persistence file from the filesystem
        :return:
        """
        try:
            self._persistence_dict = pickle.load(open(self._db_file, "rb"))
        except FileNotFoundError:
            self._persistence_dict = dict()

    def _dump_dict(self):
        """
        writes the current volatile dict to a persistent file
        :return:
        """
        pickle.dump(self._persistence_dict, open(self._db_file, "wb"))
