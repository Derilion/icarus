from icarus.skills.SuperSkill import SuperSkill
from time import sleep


class TimerSkill(SuperSkill):

    id = 'Basic Timer'
    name = "Timer Skill"
    version = "1.0"
    creator = "Derilion"
    tokens = ['timer']
    phrases = ["Set a timer for five minutes"]

    max_threads = 15
    _response = "I have set a timer for {} seconds"
    _units = [["second", 1], ["minute", 60], ["hour", 3600], ["day", 24 * 3600]]

    def main(self, message):
        timer_seconds = 0

        for unit in self._units:
            timer_seconds += self._get_token(unit[0], message)*unit[1]
        if timer_seconds == 0:
            message.send("To set a timer I need at least some time")
            return
        message.send(self._response.format(round(timer_seconds)))
        sleep(timer_seconds)
        message.send("Timer is up")

    @staticmethod
    def _get_token(unit: str, msg):
        units = unit + 's'
        if unit in msg.tokens:
            try:
                return int(msg.tokens[msg.tokens.index(unit)-1])
            except ValueError or IndexError:
                pass    # just dont leave the function
        elif units in msg.tokens:
            try:
                return int(msg.tokens[msg.tokens.index(units)-1])
            except ValueError or IndexError:
                pass    # just dont leave the function
        return 0
