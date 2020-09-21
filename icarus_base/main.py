#!/usr/bin/env python3

"""
Project Icarus

creator: derilion
date: 01.07.2019
version: 0.1a
"""

"""
TODO:
- Installer
- Database Structure
- Special Characters in *.ini 
- Setup of skills
- Configuration of Clients
- multi language support
"""

# general imports
from src.Clients.superclient import SuperClient
from src.SkillManagement.skillmanager import SkillManager
# from src.restapi import RestApi
from src.Persistence.persistence import Persistence
from logger import console_logger, icarus_logger, logging

# imports for module discovery
from importlib import import_module
import os
import sys
import inspect

CLIENT_PATH = os.path.join('.', 'src', 'Clients')


class Icarus:

    client_threads = None
    data_source = None
    skill_strategy = None
    rest_api = None

    def __init__(self):
        icarus_logger.info("Starting")
        self.data_source = Persistence()
        self.set_skill_strategy(SkillManager(self.data_source))
        self._init_clients()
        # self.rest_api = RestApi('test', self.data_source).start()

    def set_skill_strategy(self, skill_strategy: SkillManager):
        self.skill_strategy = skill_strategy

    def _init_clients(self):
        """ Discovers installed clients """
        self.client_threads = []

        # search all files in plugin path
        for file in os.listdir(CLIENT_PATH):

            if file.endswith('.py'):
                # import all files into python
                temp = file.rsplit('.py', 1)
                import_module('src.Clients.' + temp[0])

                # check if any contained classes are children of "SuperSkill"
                for name, obj in inspect.getmembers(sys.modules['src.Clients.' + temp[0]]):
                    if inspect.isclass(obj) and issubclass(obj, SuperClient) and obj is not SuperClient:
                        icarus_logger.debug("Discovered Client \"{}\"".format(temp[0]))

                        # append and init found clients
                        self.client_threads.append(obj(self.skill_strategy, self.data_source))

    def _start_clients(self):
        for client in self.client_threads:
            client.start()

    def _stop_clients(self):
        for client in self.client_threads:
            client.stop()
            client.join(1)

    def start(self):
        self._start_clients()


# thread safe init
if __name__ == "__main__":
    Icarus().start()
    # app.run(port="10080")  # iwie unschön
