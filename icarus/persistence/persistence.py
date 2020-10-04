"""
    Persistence Singleton to control persistence invocations
    Implemented as strategy to unify access
"""
from threading import Lock
from icarus.persistence.database import SuperDatabase, SerialDatabase
from icarus.persistence.configuration import IniConfiguration


class Persistence(SuperDatabase):
    _db = None
    _config = None

    _instance = None
    _instance_lock = Lock()

    def __new__(cls, *args, **kwargs):
        """
        Thread safe singleton implementation
        :param args:
        :param kwargs:
        """
        with Persistence._instance_lock:
            if Persistence._instance is None:
                if Persistence._instance is None:
                    Persistence._instance = super(Persistence, cls).__new__(cls, *args, **kwargs)
        return Persistence._instance

    def __init__(self, db: SuperDatabase = SerialDatabase(), config: IniConfiguration = IniConfiguration()):
        """
        Initialises persistence object with a specified database and configuration strategy
        :param db: database interaction handler
        :param config: configuration interaction handler
        """
        self.set_db_strategy(db)
        self.set_config_strategy(config)

    # Strategy Setters
    def set_db_strategy(self, db: SuperDatabase):
        """
        Setter to change database strategy at runtime
        :param db: database handler
        """
        self._db = db

    def set_config_strategy(self, config: IniConfiguration):
        """
        Setter to change configuration strategy at runtime
        :param config: configuraiton handler
        """
        self._config = config

    # DB interaction
    def load_table(self, table_id: str) -> dict:
        """
        Load a table saved in the database
        :param table_id: data table identifier
        :return: table as a dictionary
        """
        return self._db.load_table(table_id)

    def write_table(self, table_id: str, data: dict) -> bool:
        """
        Save a dictionary in the database
        :param table_id: identifier where data should be saved
        :param data: dictionary containing data to be saved
        :return: True if writing worked, False on error
        """
        return self._db.write_table(table_id, data)

    # Config interaction
    def get_config(self, setting_id: str, option_id: str) -> str:
        """
        Load configuration data
        :param setting_id: configuration section identifier
        :param option_id: configuration setting identifiers
        :return: setting string if found, empty string if there is none
        """
        return self._config.get_config(setting_id, option_id)
