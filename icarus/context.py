"""Message info"""
from random import randint
from icarus.logging import icarus_logger, console_logger


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
        """
        Initialises a Context object which handles information exchange between clients and skills
        :param msg: input which will be casted to string, usually a text interaction
        :param client: client reference
        :param client_attr: optional client specific information for interaction context, defaults to None
        """
        self.msg = str(msg)
        self.client = client
        self.client_attr = client_attr
        self.tokens = list()
        self.date_tokens = list()
        self.intent_tokens = list()
        self._parse()

    def set_skill(self, skill: list):
        """
        Set list of skills ordered by probability of match
        :param skill:
        :return:
        """
        self.skill = skill

    def run_next_skill(self):
        """
        Loads next skill from list of matching skills, returns if none are found
        :return:
        """
        if len(self.skill) < 1:
            # todo: log out of skills
            return
        skill = self.skill.pop(0)
        icarus_logger.debug("Running Skill {}".format(skill.name))
        console_logger.debug("Running Skill {}".format(skill.name))
        skill.append_message(self)

    def get_tokens(self):
        """
        Getter for message string tokens
        :return: list
        """
        return self.tokens

    def send(self, msg, parameters: list = None):
        """
        Sends response through client context
        :param msg: a string or list of strings
        :param parameters: formatting information which should be placed inside a format string
        :return:
        """
        if isinstance(msg, list):
            # if its a list select an option at random
            msg = msg[randint(0, len(msg) - 1)]
        # send the message with available context
        # todo: implement length mismatch error
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
