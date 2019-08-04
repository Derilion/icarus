"""
General skills required for basic fallback and identity interaction
"""

from skills.SuperSkill import SuperSkill
from random import randint
from datetime import datetime


class GreetingSkill(SuperSkill):
    name = "Greeting Skill"
    version = "1.0"
    creator = ""
    tokens = ["hello", "hi", "good", "morning", "night", "heyo", "servus", "hey"]

    _morning_responses = ["Good morning!", "Are you awake already?", "So early.."]
    _general_responses = ["Hi", "How is it going?", "Greetings to you, fellow citizen"]
    _night_responses = ["Oh, you are still awake?", "Not asleep yet", "You really should sleep"]

    def main(self, message):
        now = datetime.now()
        if 5 < now.hour < 12:
            message.send(self._morning_responses)
        elif 19 < now.hour or now.hour < 5:
            message.send(self._night_responses)
        else:
            message.send(self._general_responses)


class IDKSkill(SuperSkill):
    name = "Unknown Interaction Skill"
    version = "1.0"
    creator = "Derilion"
    tokens = []

    _responses = ["Sorry, I don't know what you mean",
                  "I am not sure I understood",
                  "I don't think I know how to provide that",
                  "Could you repeat that?"]

    def main(self, message):
        message.send(self._responses)


class TimeSkill(SuperSkill):
    name = "Time Skill"
    version = "1.0"
    creator = "derilion"
    tokens = ["date", "time", "stardate"]

    _date_response = ["It is {}, the {} of {} {}"]
    _time_Response = ["It is {}:{} {}"]
    _stardate_response = ["It is stardate {}"]

    _cochrane_const = 2063

    def main(self, message):
        #parsing

        current = datetime.now()
        year = current.year
        days_this_year = datetime(year+1, 1, 1) - datetime(year, 1, 1)
        days_gone = current - datetime(year, 1, 1)
        stardate = round(1000 * (current.year + 1 / days_this_year.days * (days_gone.days -1 + current.hour / 24 + current.minute / 1440) - self._cochrane_const), 2)
        if stardate < 0:
            stardate = stardate * -1
            stardate = str(stardate) + " before Warp flight"

        message.send(self._stardate_response[0].format(stardate))




class Keanufy(SuperSkill):
    name = "Keanufy Skill"
    version = "1.0"
    creator = "derilion"
    tokens = ["you", "are", "breathtaking"]

    def main(self, message):
        if (self.tokens[0] in message.get_tokens()) and (self.tokens[1] in message.get_tokens()) and \
                (self.tokens[2] in message.get_tokens()):
            message.send("No, you're breathtaking!")
        else:
            message.run_next_skill()

