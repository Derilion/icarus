"""
    Porcupine wake word engine wrapper
    GitHub: https://github.com/Picovoice/Porcupine
"""

import pvporcupine
import pyaudio
import struct
from icarus.clients.WakeWordEngines.superwakeword import SuperWakeWord


class Recognition(Exception):
    pass


class Porcupine(SuperWakeWord):

    def __init__(self):
        # todo: hardcoded parameters
        self.sensitivity = [0.5]

        self.handle = pvporcupine.create(keywords=['jarvis'])
        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=self.handle.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.handle.frame_length)

    def monitor_audio(self, callback):
        try:
            while True:
                pcm = self._get_next_audio_frame()
                keyword_index = self.handle.process(pcm)
                if keyword_index is not False:
                    print("Recognized Keyword")
                    raise Recognition

        except KeyboardInterrupt:
            print("stopping")

        except Recognition:
            callback()

    def _get_next_audio_frame(self):
        pcm = self.audio_stream.read(self.handle.frame_length)
        pcm = struct.unpack_from("h" * self.handle.frame_length, pcm)
        return pcm
