"""
    Icarus class
    Central program instance, controls init, thread spawning and shutdown
"""

# general imports
from icarus.clients.superclient import SuperClient
from icarus.skillmanagement.skillmanager import SkillManager
# from src.restapi import RestApi
from icarus.persistence.persistence import Persistence
from icarus.logging import icarus_logger

# imports for module discovery
from importlib import import_module
import os
import sys
import inspect

CLIENT_PATH = os.path.join(os.path.dirname(__file__), 'Clients')


class Icarus:

    client_threads = None
    data_source = None
    skill_strategy = None
    rest_api = None

    def __init__(self):
        """
        initialise basic objects: persistence and skill manager
        """
        icarus_logger.info("Starting")
        self.data_source = Persistence()
        self.set_skill_strategy(SkillManager(self.data_source))
        self._init_clients()
        # self.rest_api = RestApi('test', self.data_source).start()

    def set_skill_strategy(self, skill_strategy: SkillManager):
        """
        Can change skill strategy at runtime
        :param skill_strategy: new skill manager
        """
        self.skill_strategy = skill_strategy

    def _init_clients(self):
        """ Discovers installed clients from src.Clients and load them """
        self.client_threads = []

        # search all files in plugin path
        for file in os.listdir(CLIENT_PATH):

            if file.endswith('.py'):
                # import all files into python
                temp = file.rsplit('.py', 1)
                import_module('icarus.clients.' + temp[0])

                # check if any contained classes are children of "SuperSkill"
                for name, obj in inspect.getmembers(sys.modules['icarus.clients.' + temp[0]]):
                    if inspect.isclass(obj) and issubclass(obj, SuperClient) and obj is not SuperClient:
                        icarus_logger.debug("Discovered Client \"{}\"".format(temp[0]))

                        try:
                            # append and init found clients
                            self.client_threads.append(obj(self.skill_strategy, self.data_source))
                        except OSError:
                            icarus_logger.error("Could not load Client \"{}\"".format(obj.name))

    def _stop_clients(self):
        """ send stop request to all clients """
        for client in self.client_threads:
            client.stop()
            client.join(1)

    def start(self):
        """ Start all loaded clients """
        for client in self.client_threads:
            client.start()

