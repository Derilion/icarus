"""
    Persistence Singleton to control persistence invocations
    Implemented as strategy to unify access
"""
from threading import Lock
from src.Persistence.database import SuperDatabase, SerialDatabase
from src.Persistence.configuration import SuperConfiguration, IniConfiguration


class Persistence(SuperDatabase, SuperConfiguration):
    _db = None
    _config = None

    _instance = None
    _instance_lock = Lock()

    def __new__(cls, *args, **kwargs):
        """Thread safe singleton implementation"""
        with Persistence._instance_lock:
            if Persistence._instance is None:
                if Persistence._instance is None:
                    Persistence._instance = super(Persistence, cls).__new__(cls, *args, **kwargs)
        return Persistence._instance

    def __init__(self, db: SuperDatabase = SerialDatabase(), config: SuperConfiguration = IniConfiguration()):
        self.set_db_strategy(db)
        self.set_config_strategy(config)

    # Strategy Setters
    def set_db_strategy(self, db: SuperDatabase):
        self._db = db

    def set_config_strategy(self, config: SuperConfiguration):
        self._config = config

    # DB interaction
    def load_table(self, table_id: str) -> dict:
        return self._db.load_table(table_id)

    def write_table(self, table_id: str, data: dict) -> bool:
        return self._db.write_table(table_id, data)

    # Config interaction
    def get_config(self, setting_id: str, option_id: str) -> str:
        return self._config.get_config(setting_id, option_id)
