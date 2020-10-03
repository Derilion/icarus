"""
    Superclass for Configuration handling
"""
from appdirs import user_config_dir
import configparser
import os


TEMPLATE_FILE = os.path.join(os.path.dirname(__file__), '../resources/example.settings.ini')
CONFIG_PATH = user_config_dir('icarus', 'derilion')
CONFIG_FILE = os.path.join(CONFIG_PATH, 'settings.ini')


class IniConfiguration:
    """ Configuration implementation for ini files """

    @staticmethod
    def _check_file():
        if not os.path.exists(CONFIG_PATH):
            os.makedirs(CONFIG_PATH)
        if not os.path.isfile(CONFIG_FILE):
            with open(TEMPLATE_FILE) as source:
                with open(CONFIG_FILE, 'w') as target:
                    for line in source:
                        target.write(line)

    @staticmethod
    def get_config(config_id: str, option_id: str) -> str:
        """
            Read configuration string from ini file
            Note: could also be implemented to separate by file, not section
        :param config_id: section name
        :param option_id: setting name
        :return: string content if option was found, empty string if not
        """
        # verify file exists
        IniConfiguration._check_file()

        # load options using configparser library
        ini_parser = configparser.ConfigParser()

        try:
            ini_parser.read(CONFIG_FILE)
            return ini_parser.get(config_id, option_id)
        except configparser.Error as exception:
            print(exception.__class__.__name__ + " reading from file " + CONFIG_PATH)
            return ''
