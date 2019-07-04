from skills.SuperSkill import SuperSkill
import requests


class OpenWeatherMapsEngine:

    _API_KEY = "f0a20f3da50bbc061ccb350c1c507e78"

    def get_weather(self, location: str):
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + location + ',de&cnt=' + '1' + \
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
    tokens = ["how", "what", "weather"]

    backend = OpenWeatherMapsEngine()

    answers_regular = "The weather is {} with {} degrees Celsius"

    def main(self, message):
        print("am i here?")
        location = "wuerzburg"
        results = self.backend.get_weather(location)
        message.send(self.answers_regular.format(results[0], results[1]))






