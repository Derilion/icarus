from porcupine.binding.python.porcupine import Porcupine
from src.Clients.superclient import SuperClient
import speech_recognition as sr
from gtts import gTTS
import os
import pyaudio
import struct

LIBRARY_PATH = "./porcupine/lib/linux/x86_64/libpv_porcupine.so"  # Path to Porcupine's C library available under lib/${SYSTEM}/${MACHINE}/
MODEL_FILE_PATH = "./porcupine/lib/common/porcupine_params.pv"  # It is available at lib/common/porcupine_params.pv
KEYWORD_FILE_PATH = './{}_linux.ppn'





class SpeechClient(SuperClient):

    sensitivity = None
    handle = None
    pa = None
    audio_stream = None

    def setup(self, name: str = 'Icarus', sensitivity: float = 0.7):
        self.sensitivity = [sensitivity]
        try:
            self.setup_porcupine(name)
        except ValueError:
            print("handling error")
            os.system('./porcupine/tools/optimizer/linux/x86_64/pv_porcupine_optimizer -r ./porcupine/resources/optimizer_data -w {} -p linux -o .'.format(name))
            self.setup_porcupine(name)
        finally:
            self.pa = pyaudio.PyAudio()
            self.audio_stream = self.pa.open(
                rate=self.handle.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.handle.frame_length)

    def setup_porcupine(self, name):
        self.handle = Porcupine(LIBRARY_PATH, MODEL_FILE_PATH, keyword_file_paths=[KEYWORD_FILE_PATH.format(name)],
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
                    os.system("mpg123 ./pling.mp3")
                    self.stt()
        except KeyboardInterrupt:
            print("stopping")

        finally:
            print('stopped')

    def stt(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
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
        os.system("mpg123 tts_message.mp3")
