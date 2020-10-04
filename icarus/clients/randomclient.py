from icarus.clients.superclient import SuperClient
import time
import random


class RandomClient(SuperClient):

    def run(self):
        if False:
            i = 0
            while not self.stop_request and i < 8:
                a = random.randint(0, 9)
                self._queue_new_message(str(a))
                time.sleep(1)
                i += 1

    def send(self, message: str, client_attr):
        print("Random says: " + str(message))
