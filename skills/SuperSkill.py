from threading import Thread, Lock
from src.context import Context
import time
import random


class SuperSkill:
    """
    Skill Superclass defining interfaces and basic mechanisms

    - threading handling
    """

    # METADATA
    id: str = None                  # Skill identifier for internal operations, must not be changed
    name: str = "To Be Defined"     # Userspace name
    version: str = "0.0"            # Version string
    creator: str = "Unknown"         # Creator name
    tokens: list = []
    phrases: list = []
    max_threads = 1

    # Queues
    _message_lock: Lock = Lock()
    _messages: list = None
    _thread_lock: Lock = Lock()
    _threads: list = None

    def __init__(self, persistence):
        """
        initialise any skill
        :param persistence: persistence object for unified persistent data access
        """
        self._persistence = persistence

        # clear skill input queue
        with self._message_lock:
            self._messages = []
        # clear skill worker list
        with self._thread_lock:
            self._threads = []

        # verify required skill data is set
        if self.id is None:
            raise ValueError("Skill ID is not set, please define attribute self.id")
        self.setup()

    def main(self, message: Context):
        """
        skill main routine, needs to be overloaded by inheriting classes
        :param message: context providing client interaction and input data
        """
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
                    # run skill
                    self.skill.main(skill)
                else:
                    self.skill._message_lock.release()
                #
                # print("thread {} clear".format(self.id))
            with self.skill._thread_lock:
                # print("thread {} terminated".format(self.id))
                self.skill._threads.remove(self)

    def append_message(self, message: Context):
        """
        Add Context object to worker queue
        :param message: context object
        :return:
        """

        self._messages.append(message)

        if len(self._threads) < self.max_threads:

            active_skill = self._SkillThread(self)
            with self._thread_lock:
                self._threads.append(active_skill)
            active_skill.start()

    """ Persistence API """

    def get_config(self, setting_id: str) -> str:
        """
        Gets setting from configuration backend by skill id and setting name
        :param setting_id: setting name
        :return: setting string if found, empty string if not found
        """
        return self._persistence.get_config(self.name, setting_id)

    def save_dict(self, data: dict, identifier: str = '') -> bool:
        """
        Saves a dict into the database backend by skill identifier and table id
        :param data: data to be saved
        :param identifier: identifier of table, defaults to ''
        :return: True if saving worked, False if not
        """
        db_identifier = self.id + identifier
        return self._persistence.write_table(db_identifier, data)

    def load_dict(self, identifier: str = '') -> dict:
        """
        Loads saved data from the database
        :param identifier: table identifier, defaults to ''
        :return: filled dictionary if data is found, empty dictionary if nothing is loaded
        """
        db_identifier = self.id + identifier
        return self._persistence.load_table(db_identifier)

    """ Skill init hook """

    def setup(self):
        """
        Method if initial setup is required before skill actually is used
        - Overload this method to do a setup of your skill before actual runtime
        """
        pass


class EchoSkill(SuperSkill):
    """
    Skill which returns the input after a delay
    """

    id = 'basic repeat skill'
    name = "Echo"
    version = "1.0"
    creator = "Derilion"
    tokens = ['say', 'repeat', 'echo']
    phrases = ["say this", "repeat me", "echo me"]

    max_threads = 2

    def main(self, message):
        time.sleep(1)
        data = self.load_dict()
        if 'ctr' in data:
            data['ctr'] += 1
        else:
            data['ctr'] = 1
        self.save_dict(data)
        print("used for {} times".format(data['ctr']))
        result = message.msg.lower()
        if "repeat" in result:
            result = result.split("repeat", 1)[1]
        elif "say" in result:
            result = result.split("say", 1)[1]
        elif "echo" in result:
            result = result.split("echo", 1)[1]

        message.send(result)
