from SimConnect import *

from conditionaltrigger import ConditionalTrigger

class SingleEvent(object):
    def __init__(self, _ae: AircraftEvents, _aq: AircraftRequests, _eventname, _type="auto", _value=0, _description=""):
        self.eventname = _eventname
        self.type = _type
        self.value = _value
        self.description = _description
        if (_type == "manual"):
            self.event = Event(_eventname.encode(), _ae.sm) #manual event with forced value
        elif _type == "condition":
            self.event = ConditionalTrigger(_eventname, _ae, _aq)
        else:
            self.event = _ae.find(_eventname) #autofind event
            

    def __call__(self, value=0):
        if self.type == "manual":
            self.event(self.value)
        else:
            self.event(value)
           

class EventQueue(object):

    def __init__(self):
        self.event_list = []

    def __call__(self, value=0):
        for event in self.event_list:
            if event:
                event(value)

    def add(self, _event: SingleEvent):
        self.event_list.append(_event)
