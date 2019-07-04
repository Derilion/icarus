from src.Clients.superclient import SuperClient
import speech_recognition as sr
from gtts import gTTS
import os


class SpeechClient(SuperClient):

    def run(self):
        while not self.stop_request:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Speak:")
                audio = r.listen(source)

            try:
                print("You said " + r.recognize_google(audio))
                self._queue_new_message(r.recognize_google(audio))
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

    def send(self, message: str, client_attr):
        tts = gTTS(text=message, lang='en')
        tts.save("tts_message.mp3")
        os.system("mpg123 tts_message.mp3")
