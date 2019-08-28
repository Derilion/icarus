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

from src.persistence import Persistence

from porcupine.binding.python.porcupine import Porcupine
import pyaudio
import struct

import pyttsx3

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


def test_pers():
    a = Persistence()
    a.register_configuration("test", "subtest", "noval")
    a.register_configuration("test", "subtester", "12")
    a.register_configuration("abc", "def", "ghi")
    a.load_config()
    a.show_config()


#library_path = "./porcupine/lib/linux/x86_64/libpv_porcupine.so"
#model_path = "./porcupine/lib/common/porcupine_params.pv"
#keyword_path = "./Jarvis_linux.ppn"
#sensitivity = 0.5
#handle = Porcupine(library_path, model_path, keyword_file_paths=[keyword_path], sensitivities=[sensitivity])
#pa = pyaudio.PyAudio()
#audio_stream = pa.open(
#        rate=handle.sample_rate,
#        channels=1,
#        format=pyaudio.paInt16,
#        input=True,
#        frames_per_buffer=handle.frame_length
#)


def test_porcupine():
    while True:
        pcm = get_next_audio_frame()
        keyword_index = handle.process(pcm)
        if keyword_index is not False:
            # detection event logic/callback
            print("recognized")


def get_next_audio_frame():
    pcm = audio_stream.read(handle.frame_length)
    pcm = struct.unpack_from("h" * handle.frame_length, pcm)
    return pcm


def tts(text: str):
    engine = pyttsx3.init()
    engine.say(text)
    engine.setProperty('rate', 120)
    engine.setProperty('volume', 1)
    engine.runAndWait()


# thread safe init
if __name__ == "__main__":
    # test_pers()
    # test_porcupine()
    # tts("test")
    Icarus().start()
