from icarus.skills.SuperSkill import SuperSkill
import caldav
from datetime import datetime, timezone, timedelta, date
from icalendar import Calendar


class CalDavSkill(SuperSkill):

    id = 'caldav'
    name = "CalDav Skill"
    creator = "Derilion"
    version = "1.0"
    tokens = ["calendar", "appointment"]
    phrases = ["Tell me my appointments for today", "What are my appointments", "What does my calendar say"]

    _user = None
    _password = None
    _url = None

    _found_str = "Found {} in {} {}. " # bla in bla minutes

    def setup(self):
        self._user = self.get_config("user")
        self._password = self.get_config("password")
        self._url = self.get_config("calendar url")

    def main(self, message):
        response = ""
        response_list = list()
        client = caldav.DAVClient(self._url, username=self._user, password=self._password)
        principal = client.principal()
        if len(message.date_tokens) == 0:
            startdate = datetime.now()
        else:
            startdate = message.date_tokens[0]
        enddate = startdate + timedelta(days=1)
        results = []

        for calendar in principal.calendars():
            # print("found calendar " + calendar.name)
            results += calendar.date_search(startdate, enddate)
            # for event in calendar.events():
            #    ical_data = self.str_to_dict(event.data)
            #    print(ical_data["SUMMARY"])

        for result in results:
            cal = Calendar.from_ical(result.data)
            for e in cal.walk('vevent'):
                response_list.append([e.get('summary'), e.get('dtstart')])

        now = datetime.now(timezone.utc)
        for response_item in response_list:
            # calc timedelta and unit
            if type(response_item[1].dt) == date:
                response_item[1].dt = datetime.combine(response_item[1].dt, datetime.min.time(), timezone.utc)

            temp = response_item[1].dt - now
            response_item[1] = temp
            print([response_item[0], temp//3600])
            if temp.days != 0:
                response += self._found_str.format(response_item[0], temp.days, "days")
            elif temp.seconds//3600 > 0:
                response += self._found_str.format(response_item[0], temp.seconds//3600, "hours")
            elif temp.seconds // 60 > 0:
                response += self._found_str.format(response_item[0], temp.seconds // 60, "minutes")
            else:
                pass

        message.send(response)
