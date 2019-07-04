#!/usr/bin/env python3

"""
Project Icarus

creator: derilion
date: 01.07.2019
version: 0.1a
"""

# imports
from src.Clients.telegramclient import TelegramClient
from src.Clients.randomclient import RandomClient
from src.Clients.cliclient import CLIClient
from src.datasources import DataSource
from src.skillstrategy import SkillStrategy


class Icarus:

    client_threads = None
    data_source = None
    skill_strategy = None

    def __init__(self):
        self.load_data_source(DataSource())
        self.set_skill_strategy(SkillStrategy())
        self._init_clients()

    def load_data_source(self, data_source: DataSource):
        self.data_source = data_source

    def set_skill_strategy(self, skill_strategy: SkillStrategy):
        self.skill_strategy = skill_strategy

    def _init_clients(self):
        self.client_threads = []
        # self.client_threads.append(CLIClient(self.skill_strategy))
        # self.client_threads.append(RandomClient(self.skill_strategy))
        self.client_threads.append(TelegramClient(self.skill_strategy))
        # self.client_threads.append(SpeechClient(self.skill_strategy))

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
