from icarus.skills.SuperSkill import SuperSkill
import requests


class OpenWeatherMapsEngine:

    _API_KEY = None

    def __init__(self, token):
        self._API_KEY = token

    def get_weather(self, location: str):
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + location + '&cnt=' + '1' + \
              '&units=metric&appid=' + self._API_KEY
        response = requests.get(url)
        if response.status_code == 200:
            # print(response.content)
            decoded = response.json()
            weather = decoded['weather'][0]['main']
            temperature = round(decoded['main']['temp'], 1)
        else:
            # logging.error("connection to weather failed")
            return None

        return [weather, temperature]


class WeatherSkill(SuperSkill):

    id = 'Weather Skill'
    name = "Weather Skill"
    version = "1.0"
    creator = "derilion"
    tokens = ["weather"]
    phrases = ["Will there be rain", "What is the weather in london", "Will it rain today"]

    backend = None
    _api_token = None
    _default_location = None

    answers_regular = "The weather is {} with {} degrees Celsius"
    answers_location = "The weather in {} is {} with {} degrees Celsius"
    answer_no_connection = ["Sorry, the server doesn't want to respond",
                            "It seems the server does not want to talk to me"]

    def setup(self):
        self._api_token = self.get_config('token')
        self._default_location = self.get_config('default location')
        self.backend = OpenWeatherMapsEngine(self._api_token)

    def main(self, message):
        try:
            index = message.tokens.index("in")
            location = message.tokens[index+1]
        except ValueError:
            location = self._default_location
        finally:
            results = self.backend.get_weather(location)
            if results is not None and location != self._default_location:
                message.send(self.answers_location.format(location, results[0], results[1]))
            elif results is not None:
                message.send(self.answers_regular.format(results[0], results[1]))
            else:
                message.send(self.answer_no_connection)






