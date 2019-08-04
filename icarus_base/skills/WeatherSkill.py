from skills.SuperSkill import SuperSkill
import requests


class OpenWeatherMapsEngine:

    _API_KEY = None  # "f0a20f3da50bbc061ccb350c1c507e78"

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

    name = "Weather Skill"
    version = "1.0"
    creator = "derilion"
    tokens = ["weather"]
    config = None

    backend = None

    answers_regular = "The weather is {} with {} degrees Celsius"
    answers_location = "The weather in {} is {} with {} degrees Celsius"
    answer_no_connection = "Sorry, the server doesn't want to respond"

    def setup(self):
        self.register_config("token")
        self.register_config("default location")
        self.config = self.get_config()
        self.backend = OpenWeatherMapsEngine(self.config["token"])
        # print("here i am")

    def main(self, message):
        try:
            index = message.tokens.index("in")
            location = message.tokens[index+1]
        except ValueError:
            location = self.config["default location"]
        finally:
            results = self.backend.get_weather(location)
            if results is not None and location != self.config["default location"]:
                message.send(self.answers_location.format(location, results[0], results[1]))
            elif results is not None:
                message.send(self.answers_regular.format(results[0], results[1]))
            else:
                message.send(self.answer_no_connection)






