"""Message info"""
from random import randint
from datetime import datetime, timedelta, timezone
from logger import icarus_logger, console_logger


class Context:
    """
    The object transporting the message and metadata for each user query

    todo: add parsing function
    todo: remove "a", "is", "I", ..
    todo: lemmatize all words (if possible)
    todo: alle dopplungen entfernen
    """

    msg: str = None
    skill: list = None
    client = None
    client_attr: dict = None
    tokens: list = None
    date_tokens: list = None    # list of datetime objects if something is found
    intent_tokens: list = None  # intents if they are found

    def __init__(self, msg, client, client_attr: dict = None):
        self.msg = str(msg)
        self.client = client
        self.client_attr = client_attr
        self.tokens = list()
        self.date_tokens = list()
        self.intent_tokens = list()
        self._parse()

    def set_skill(self, skill: list):
        self.skill = skill

    def run_next_skill(self):
        skill = self.skill.pop(0)
        icarus_logger.debug("Running Skill {}".format(skill.name))
        console_logger.debug("Running Skill {}".format(skill.name))
        skill.append_message(self)

    def get_tokens(self):
        """
        Getter for tokens
        :return: list
        """
        return self.tokens

    def send(self, msg, parameters: list = None):
        if isinstance(msg, list):
            # if its a list select an option at random
            msg = msg[randint(0, len(msg) - 1)]
        # send the message with available context
        if parameters:
            msg = msg.format(*parameters)
        self.client.send(str(msg), self.client_attr)

    def _parse(self):
        """
        Creates a token list should be removed / changed. Async additional parsing? Web backend? POS tagging?
        """

        local_tokens = self.msg.lower().split()
        for token in local_tokens:
            if token not in self.tokens:
                self.tokens.append(token)

        # if "today" in local_tokens:
        #     self.date_tokens.append((datetime.now(timezone.utc)).replace(hour=0, minute=0, second=0, microsecond=0))
        # if "tomorrow" in local_tokens:
        #     self.date_tokens.append(datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        #                             + timedelta(days=1))
        # if "yesterday" in local_tokens:
        #     self.date_tokens.append(datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        #                             - timedelta(days=1))
        #
        # if len(self.date_tokens) > 0:
        #     icarus_logger.debug("Found date tokens " + str(self.date_tokens))

    def __str__(self):
        return self.msg
