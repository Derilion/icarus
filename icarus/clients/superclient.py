from threading import Thread
from icarus.skillmanagement.skillmanager import SkillManager
from icarus.persistence.persistence import Persistence
from icarus.context import Context
from icarus.logging import icarus_logger
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
        if message == "":
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
        """
        Sends a message using the defined client
        :param message: string to send using the client
        :param client_attr: additional client information
        :return:
        """
        pass

    def notify(self, client_attr, notification_text: str = ''):
        """
        Sends a notification on supporting clients, sends a standard message as default
        :param client_attr: additional client information
        :param notification_text: additional information string to be sent as message
        :return:
        """
        if notification_text == '':
            notification_text = 'Beep'
        self.send(notification_text, client_attr)


class ClientStopException(Exception):
    icarus_logger.debug("Client stopped")
