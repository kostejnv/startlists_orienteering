import json
from test_platform.entities.event import Event


class Event_manager:
    def __init__(self, event_f):
        self.event = json.load(event_f)

    def get_event(self): # get general information about event
        name = self.event["Name"]
        id = self.event["ID"]
        date = self.event["Date"]
        discipline = self.event["Discipline"]["ShortName"]
        region = self.event["Region"]
        return Event(id, name, date, discipline, region)
