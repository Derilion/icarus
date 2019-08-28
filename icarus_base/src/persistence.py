"""A singleton object to unify persistance and configuration access"""
import pickle
import configparser
from threading import Lock

CONFIG_PATH = "./config.ini"
DB_FILEPATH = "./persistence.va"

instance = None

"""
persistence workflow:
1. register all config vars
2. load all config vars
3. init skill
"""


class ConfigIni:
    """Implements Ini config reading"""

    _config_path = None

    def __init__(self, config_path=CONFIG_PATH):
        self._config_path = config_path

    def load_config(self, config_dict: dict):
        """reads all options from the config file"""

        # init parser
        ini_parser = configparser.ConfigParser()
        ini_parser.read(self._config_path)

        # read all options
        for section in config_dict:
            for variable in config_dict[section]:
                config_dict[section][variable] = self.read_option(ini_parser, section, variable,
                                                                  config_dict[section][variable])

        # write changes [e.g. new settings not existing yet]
        with open(self._config_path, 'w') as ini_file:
            ini_parser.write(ini_file)

    @staticmethod
    def read_option(ini_parser: configparser.ConfigParser, section: str, option: str, default: str = "") -> str:
        """Read every single option and add not existing ones"""
        result = default
        try:
            result = ini_parser.get(section, option)
        except configparser.NoSectionError:
            ini_parser.add_section(section)
            ini_parser.set(section, option, default)
        except configparser.NoOptionError:
            ini_parser.set(section, option, default)
        finally:
            return result


class SimpleDB:
    """
    a simple persistence without a heavy db implementation
    """
    _db_file = None
    _persistence_dict = None
    _thread_lock = Lock()

    def __init__(self, filepath: str = DB_FILEPATH):
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


class Persistence:

    # todo: implement singleton
    """
    register all variables with [name, type]
    register function
    set function
    get function
    db holds private and public info
    config holds public info only
    type can be an enum, str, int, password
    name must be a string
    get function returns dictionary with all saved values
    """

    config = None
    db = None

    _config_db_key = "CONFIG"
    _config_dict: dict = None
    _persistence_dict: dict = None

    def __init__(self, config_handler=ConfigIni(), db_handler=SimpleDB()):
        self.config = config_handler
        self.db = db_handler
        self._config_dict = dict()
        self._persistence_dict = dict()

    def load_config(self):
        """Refresh the current config dict"""
        self.config.load_config(self._config_dict)
        temp = self.load_persistent_dict(self._config_db_key)
        # todo: merge dicts

    def get_config(self, section: str) -> dict:
        """Load a specific config section"""
        # load config on demand
        self.load_config()
        return self._config_dict[section]

    def register_persistence(self, name: str, parent: str, default="", private=""):
        """register new persistent variables
        currently unused
        """
        pass

    def save_persistent_dict(self, key: str, data: dict):
        """Saves a dictionary persistently on the current backend"""
        self.db.save_dict(key, data)

    def load_persistent_dict(self, key: str):
        """returns the current dictionary from the backend"""
        return self.db.load_dict(key)

    def register_configuration(self, parent: str, name: str, default: str = ""):
        """register new configuration variables"""
        # check stuff first
        if self._config_dict.get(parent) is None:
            self._config_dict[parent] = dict()
        self._config_dict[parent][name] = default
        self.save_persistent_dict(self._config_db_key, self._config_dict)

    def show_config(self):
        """readable printout of the loaded configuration"""
        ret_str = "\t{}: {}"

        for section in self._config_dict:
            print("[{}]".format(section))
            for variable in self._config_dict[section]:
                print(ret_str.format(variable, self._config_dict[section][variable]))



