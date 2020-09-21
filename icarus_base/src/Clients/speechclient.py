from src.Clients.superclient import SuperClient
import speech_recognition as sr
from gtts import gTTS
import os
import pyaudio
import struct
import platform
import pvporcupine
from playsound import playsound
from logger import logging, icarus_logger

PLING_MP3 = os.path.join('.', 'pling.mp3')


class SpeechClient(SuperClient):

    sensitivity = None
    handle = None
    pa = None
    audio_stream = None

    def setup(self, name: str = 'jarvis', sensitivity: float = 0.5):

        self.sensitivity = [sensitivity]

        self.handle = pvporcupine.create(keywords=[name])
        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=self.handle.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.handle.frame_length)

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
                    self.stt()
        except KeyboardInterrupt:
            print("stopping")

        finally:
            print('stopped')

    def _play_init(self):
        try:
            playsound(PLING_MP3)
        except ModuleNotFoundError:
            # arch has a problem with python-gobject, using mpg123 as fallback
            os.system("mpg123 ./pling.mp3 >/dev/null 2>&1")

    def stt(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 0.5)
            self._play_init()
            print("Speak:")
            audio = r.listen(source, timeout=2, phrase_time_limit=4)

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
            os.system("mpg123 tts_message.mp3 >/dev/null 2>&1")
        if os.path.isfile("tts_message.mp3"):
            os.remove("tts_message.mp3")
