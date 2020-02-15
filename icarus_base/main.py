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
"""

# imports
from src.Clients.telegramclient import TelegramClient
from src.Clients.randomclient import RandomClient
from src.Clients.cliclient import CLIClient
from src.Clients.speechclient import SpeechClient
from src.skillstrategy import SkillStrategy
from src.restapi import RestApi, PERSISTENCE
from src.persistence import Persistence
from logger import console_logger, icarus_logger, logging

from porcupine.binding.python.porcupine import Porcupine
import pyaudio
import struct

import pyttsx3


class Icarus:

    client_threads = None
    data_source = None
    skill_strategy = None
    rest_api = None

    def __init__(self):
        # self.load_data_source(Persistence())
        self.data_source = PERSISTENCE
        self.set_skill_strategy(SkillStrategy(self.data_source))
        self._init_clients()
        self.rest_api = RestApi('test', self.data_source).start()

    def load_data_source(self, data_source: Persistence):
        self.data_source = data_source

    def set_skill_strategy(self, skill_strategy: SkillStrategy):
        self.skill_strategy = skill_strategy

    def _init_clients(self):
        self.client_threads = []
        # self.client_threads.append(CLIClient(self.skill_strategy))
        # self.client_threads.append(RandomClient(self.skill_strategy))
        self.client_threads.append(TelegramClient(self.skill_strategy))
        self.client_threads.append(SpeechClient(self.skill_strategy))

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
