"""A singleton object to unify persistance and configuration access"""

CONFIG_PATH = "./config.ini"

instance = None

# single stuff: register_Var(name, mother_func, default_val, private, is_password, is_username)


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

    config_dict: dict = None
    persistence_dict: dict = None

    def __init__(self):
        self.set_config(ConfigIni())
        self.config_dict = dict()
        self.persistence_dict = dict()

    def set_config(self, config):
        self.config = config

    def load_config(self):
        self.config.load_config(self.config_dict)

    def get_config(self, section: str)->dict:
        # load config on demand
        self.load_config()
        return self.config_dict[section]

    def set_db(self, db):
        self.db = db

    def register_persistence(self, name: str, parent: str, default="", private=""):
        pass

    def register_configuration(self, parent: str, name: str, default: str = ""):
        # check stuff first
        if self.config_dict.get(parent) is None:
            self.config_dict[parent] = dict()
        self.config_dict[parent][name] = default

    def show_config(self):
        ret_str = "\t{}: {}"

        for section in self.config_dict:
            print("[{}]".format(section))
            for variable in self.config_dict[section]:
                print(ret_str.format(variable, self.config_dict[section][variable]))



import configparser


class ConfigIni:
    """Implements Ini config reading"""

    def __init__(self):
        pass

    def load_config(self, config_dict: dict):

        # init parser
        ini_parser = configparser.ConfigParser()
        ini_parser.read(CONFIG_PATH)

        # read all options
        for section in config_dict:
            for variable in config_dict[section]:
                config_dict[section][variable] = self.read_option(ini_parser, section, variable,
                                                                  config_dict[section][variable])

        # write changes
        with open(CONFIG_PATH, 'w') as ini_file:
            ini_parser.write(ini_file)

    @staticmethod
    def read_option(ini_parser: configparser.ConfigParser, section: str, option: str, default: str = "") -> str:
        """Read every single option"""
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




