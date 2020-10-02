"""
    Superclass for Configuration handling
"""
import configparser
import os


class SuperConfiguration:

    def get_config(self, config_id: str, option_id: str) -> str:
        pass


CONFIG_PATH = "."
DEFAULT_FILE = "settings"


class IniConfiguration(SuperConfiguration):
    """ Configuration implementation for ini files """

    def get_config(self, config_id: str, option_id: str) -> str:
        """
            Read configuration string from ini file
            Note: could also be implemented to separate by file, not section
        :param config_id: section name
        :param option_id: setting name
        :return: string content if option was found, empty string if not
        """

        # load options using configparser library
        ini_parser = configparser.ConfigParser()

        try:
            ini_parser.read(os.path.join(CONFIG_PATH, DEFAULT_FILE + '.ini'))
            return ini_parser.get(config_id, option_id)
        except configparser.Error as exception:
            # todo: add logging
            print(exception.__class__.__name__ + " reading from file " + os.path.join(CONFIG_PATH, DEFAULT_FILE +
                                                                                      '.ini'))
            return ''
