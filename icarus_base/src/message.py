"""Message info"""
from random import randint

class MessageInfo:
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

    def __init__(self, msg, client, client_attr: dict = None):
        self.msg = str(msg)
        self.client = client
        self.client_attr = client_attr
        self.tokens = list()
        self._parse()

    def set_skill(self, skill: list):
        self.skill = skill

    def run_next_skill(self):
        skill = self.skill.pop(0)
        print("Running Skill {}".format(skill.name))
        skill.append_message(self)

    def get_tokens(self):
        """
        Getter for tokens
        :return: list
        """
        return self.tokens

    def send(self, msg):
        if isinstance(msg, list):
            # if its a list select an option at random
            msg = msg[randint(0, len(msg) - 1)]
        # send the message with available context
        self.client.send(str(msg), self.client_attr)

    def _parse(self):
        """
        Creates a token list
        """

        local_tokens = self.msg.lower().split()
        for token in local_tokens:
            if token not in self.tokens:
                self.tokens.append(token)

    def __str__(self):
        return self.msg
