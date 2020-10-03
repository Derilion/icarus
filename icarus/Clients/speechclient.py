from icarus.Clients.superclient import SuperClient
import speech_recognition as sr
from gtts import gTTS
import os
import platform
from playsound import playsound
from icarus.logging import icarus_logger
try:
    from icarus.Clients.WakeWordEngines.porcupine import Porcupine
except OSError:
    icarus_logger.warning('Tried using porcupine with windows')

PLING_MP3 = os.path.join(os.path.dirname(__file__), '../resources/pling.mp3')


class SpeechClient(SuperClient):

    sensitivity = None
    handle = None
    pa = None
    audio_stream = None
    wake_word_handler = None

    def __init__(self, skill_handler, persistence):
        if platform.system() == 'Windows':
            raise OSError
        super().__init__(skill_handler, persistence)

    def setup(self):
        self.wake_word_handler = Porcupine()

    def run(self):
        self.setup()
        while True:
            self.wake_word_handler.monitor_audio(self.stt)

    @staticmethod
    def _play_init():
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
        if self.persistence.get_config('SpeechClient', 'morse'):
            message = SpeechClient._message2morse(message)
        tts = gTTS(text=message, lang='en')
        tts.save("tts_message.mp3")
        if platform.system().lower() == 'windows':
            playsound("tts_message.mp3")
        else:
            os.system("mpg123 tts_message.mp3 >/dev/null 2>&1")
        if os.path.isfile("tts_message.mp3"):
            os.remove("tts_message.mp3")

    @staticmethod
    def _message2morse(message):
        # Dictionary representing the morse code chart
        MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                            'C':'-.-.', 'D':'-..', 'E':'.',
                            'F':'..-.', 'G':'--.', 'H':'....',
                            'I':'..', 'J':'.---', 'K':'-.-',
                            'L':'.-..', 'M':'--', 'N':'-.',
                            'O':'---', 'P':'.--.', 'Q':'--.-',
                            'R':'.-.', 'S':'...', 'T':'-',
                            'U':'..-', 'V':'...-', 'W':'.--',
                            'X':'-..-', 'Y':'-.--', 'Z':'--..',
                            '1':'.----', '2':'..---', '3':'...--',
                            '4':'....-', '5':'.....', '6':'-....',
                            '7':'--...', '8':'---..', '9':'----.',
                            '0':'-----', ', ':'--..--', '.':'.-.-.-',
                            '?':'..--..', '/':'-..-.', '-':'-....-',
                            '(':'-.--.', ')':'-.--.-'}
        morse = ''
        for letter in message.upper():
            if letter == ' ':
                morse += ' '
            elif letter in MORSE_CODE_DICT:
                morse += MORSE_CODE_DICT[letter] + ' '
            else:
                morse += ''
        morse = morse.replace('.', "Beep")
        morse = morse.replace('_', "Beeeeeeep")
        return morse
