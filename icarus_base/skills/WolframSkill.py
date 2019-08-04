from skills.SuperSkill import SuperSkill
import requests

TOKEN = "RKR533-H4G588JTUR"


class WolframSkill(SuperSkill):

    name = "Wolfram Skill"
    version = "1.0"
    creator = "Derilion"
    tokens = {"Wolfram", "Alpha"}

    _token = None
    _api_url = "http://api.wolframalpha.com/v1/spoken"

    def setup(self):
        self.register_config("token")
        self._token = self.get_config()["token"]

    def main(self, message):
        params = {
            'appid': self._token,
            'i': message.msg,
            'units': 'metric',
            'timeout': 2
        }
        resp = requests.get(self._api_url, params=params)

        if resp.status_code != 200:
            message.run_next_skill()
        else:
            message.send(resp.text)
