from threading import Thread
from src.SkillManagement.skillmanager import SkillManager
from src.Persistence.persistence import Persistence
from src.message import MessageInfo
from logger import icarus_logger
import random


class SuperClient(Thread):

    id = None
    stop_request = False
    skill_handler = None
    persistence = None

    def __init__(self, skill_handler: SkillManager, persistence: Persistence):
        Thread.__init__(self)
        self.id = random.randint(0, 999)
        self.skill_handler = skill_handler
        self.persistence = persistence

    def _queue_new_message(self, message: str, client_opt: dict = None):
        # print("Added new Message: {} to queue of length {}".format(message, len(self.inbound_fifo)))
        if message is "":
            return
        message = MessageInfo(message, self, client_opt)

        self.skill_handler.find_skills(message)
        message.run_next_skill()

    def stop(self):
        self.stop_request = True

    def send(self, message: str, client_attr):
        pass


class ClientStopException(Exception):
    icarus_logger.debug("Client stopped")
