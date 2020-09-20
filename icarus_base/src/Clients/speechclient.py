from porcupine.binding.python.porcupine import Porcupine
from src.Clients.superclient import SuperClient
import speech_recognition as sr
from gtts import gTTS
import os
import pyaudio
import struct
import platform
from playsound import playsound
from logger import logging

LIBRARY_PATH = os.path.join('.', 'porcupine', 'lib', '{0}', '{1}', '{2}')               # Path to Porcupine's C library
MODEL_FILE_PATH = os.path.join('.', 'porcupine', 'lib', 'common', 'porcupine_params.pv')
LICENSE_CREATION = os.path.join('.', 'porcupine', 'tools', 'optimizer', '{0}', '{1}', 'pv_porcupine_optimizer') \
                   + ' -r ' + os.path.join('.', 'porcupine', 'resources', 'optimizer_data') + ' -w {2} -p {0} -o .'
KEYWORD_FILE_PATH = './{0}_{1}.ppn'
PLING_MP3 = os.path.join('.', 'pling.mp3')


class SpeechClient(SuperClient):

    sensitivity = None
    handle = None
    pa = None
    audio_stream = None

    def setup(self, name: str = 'Jarvis', sensitivity: float = 0.5):
        self.sensitivity = [sensitivity]
        system = self.get_system_info()
        try:
            self.setup_porcupine(name, system)
        except (ValueError, OSError):
            print("handling error")
            os.system(LICENSE_CREATION.format(system["os"], system["processor"], name))
            self.setup_porcupine(name, system)
        finally:
            self.pa = pyaudio.PyAudio()
            self.audio_stream = self.pa.open(
                rate=self.handle.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.handle.frame_length)

    @staticmethod
    def get_system_info():
        result = dict()
        result["os"] = platform.system().lower()
        result["processor"] = platform.machine()
        if result["os"] == "linux" and "arm" in result["processor"]:
            result["lib"] = "raspberry-pi"
            result["processor"] = "cortex-a7"
        else:
            result["lib"] = result["os"]
        return result

    def setup_porcupine(self, name, system):
        if system["os"] == 'windows':
            self.handle = Porcupine(LIBRARY_PATH.format(system["lib"], system["processor"], 'libpv_porcupine.dll'),
                                    MODEL_FILE_PATH, keyword_file_paths=[KEYWORD_FILE_PATH.format(name, system["os"])],
                                    sensitivities=self.sensitivity)
        else:
            self.handle = Porcupine(LIBRARY_PATH.format(system["lib"], system["processor"], 'libpv_porcupine.so'),
                                    MODEL_FILE_PATH, keyword_file_paths=[KEYWORD_FILE_PATH.format(name, system["os"])],
                                    sensitivities=self.sensitivity)

    def _get_next_audio_frame(self):
        pcm = self.audio_stream.read(self.handle.frame_length)
        pcm = struct.unpack_from("h" * self.handle.frame_length, pcm)
        return pcm

    def run(self):
        self.setup()
        try:
            while not self.stop_request:
                pcm = self._get_next_audio_frame()
                keyword_index = self.handle.process(pcm)
                if keyword_index is not False:
                    if platform.system().lower() == 'windows':
                        playsound(PLING_MP3)
                    else:
                        os.system("mpg123 ./pling.mp3")
                    self.stt()
        except KeyboardInterrupt:
            print("stopping")

        finally:
            print('stopped')

    def stt(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Speak:")
            audio = r.listen(source)

        try:
            result = r.recognize_google(audio)
            print("You said " + result)
            self._queue_new_message(result)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

    def send(self, message: str, client_attr):
        tts = gTTS(text=message, lang='en')
        tts.save("tts_message.mp3")
        if platform.system().lower() == 'windows':
            playsound("tts_message.mp3")
        else:
            os.system("mpg123 tts_message.mp3")
        if os.path.isfile("tts_message.mp3"):
            os.remove("tts_message.mp3")
