from threading import Thread, Lock
from src.persistence import Persistence
import time
import random


class SuperSkill:
    """
    Skill Superclass defining interfaces and basic mechanisms

    - threading handling
    """

    # METADATA
    name: str = "To Be Defined"
    version: str = "0.0"
    creator: str = "Nobody"
    tokens: list = []
    max_threads = 1

    # Queues
    _message_lock: Lock = Lock()
    _messages: list = None
    _thread_lock: Lock = Lock()
    _threads: list = None

    def __init__(self):
        self.persistence = Persistence()
        with self._message_lock:
            self._messages = []
        with self._thread_lock:
            self._threads = []

        self.setup()

    def main(self, message):
        raise ValueError("Skill functionality is not defined")

    class _SkillThread(Thread):
        """
        Embedded Thread to implement a worker solution
        """

        def __init__(self, skill):
            Thread.__init__(self)
            self.skill = skill
            self.id = random.randint(0, 99)

        def run(self):
            """
            Main execution of Thread
            Pulls threadsafe messages from FIFO and executes the skill
            :return:
            """

            while len(self.skill._messages) > 0:
                self.skill._message_lock.acquire()
                if len(self.skill._messages) > 0:
                    # print("thread {} acting".format(self.id))
                    skill = self.skill._messages.pop(0)
                    self.skill._message_lock.release()
                    self.skill.main(skill)
                else:
                    self.skill._message_lock.release()
                #
                # print("thread {} clear".format(self.id))
            with self.skill._thread_lock:
                # print("thread {} terminated".format(self.id))
                self.skill._threads.remove(self)

    def append_message(self, message):

        self._messages.append(message)

        if len(self._threads) < self.max_threads:

            active_skill = self._SkillThread(self)
            with self._thread_lock:
                self._threads.append(active_skill)
            active_skill.start()

    def get_tokenlength(self):
        return len(self.tokens)

    def register_config(self, name: str, default_val: str = ""):
        self.persistence.register_configuration(self.name, name, default_val)

    def get_config(self) -> dict:
        return self.persistence.get_config(self.name)

    def setup(self):
        pass


class EchoSkill(SuperSkill):
    """
    Skill which returns the input after a delay
    """

    name = "Echo"
    version = "1.0"
    creator = "Derilion"
    tokens = ['say', 'repeat', 'echo']

    max_threads = 2

    def main(self, message):
        time.sleep(1)
        message.send(message.msg)
