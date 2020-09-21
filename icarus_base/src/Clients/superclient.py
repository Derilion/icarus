from threading import Thread
from src.SkillManagement.skillmanager import SkillManager
from src.Persistence.persistence import Persistence
from src.context import Context
from logger import icarus_logger
import random


class SuperClient(Thread):
    """
    Client Superclass, all inheriting classes can be loaded as clients
    """

    id = None
    stop_request = False
    skill_handler = None
    persistence = None

    def __init__(self, skill_handler: SkillManager, persistence: Persistence):
        """

        :param skill_handler:
        :param persistence:
        """
        Thread.__init__(self)
        self.id = random.randint(0, 999)
        self.skill_handler = skill_handler
        self.persistence = persistence

    def _queue_new_message(self, message: str, client_opt: dict = None):
        """
        Queues an input to be processed by skills
        :param message: String formatted input text
        :param client_opt: Optional client context information
        :return:
        """
        # print("Added new Message: {} to queue of length {}".format(message, len(self.inbound_fifo)))
        if message is "":
            return
        message = Context(message, self, client_opt)

        self.skill_handler.find_skills(message)
        message.run_next_skill()

    def stop(self):
        """
        Set a stop request a client should implement for a thread safe clean stop
        :return:
        """
        self.stop_request = True

    def send(self, message: str, client_attr):
        pass


class ClientStopException(Exception):
    icarus_logger.debug("Client stopped")
