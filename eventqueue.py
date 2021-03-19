from SimConnect import Event

from conditionalrunner import ConditionalRunner
from globalstorage import GlobalStorage


class SingleEvent:
    def __init__(self, event_name, event_type="auto", value=0):
        self._event_name = event_name
        self._event_type = event_type
        self._value = value
        self._ae = GlobalStorage().aircraft_events
        self._aq = GlobalStorage().aircraft_requests
        self._event = None

        if event_type == "manual":
            self._event = Event(event_name.encode(), self._ae.sm)  # manual event with forced value
        elif event_type == "condition":
            self._event = ConditionalRunner(event_name)
        elif event_type == "condition-file":
            self._event = ConditionalRunner("", event_name)
        else:
            self._event = self._ae.find(event_name)  # auto find event
            if self._event is None:
                print(f"WARNING: Event {event_name}, was not found in simconnect list. Using a manual binding")
                self._event = Event(event_name.encode(), self._ae.sm)

    def __call__(self, value=0):
        if self._event_type == "manual":
            self._event(self._value)
        else:
            self._event(value)


class EventQueue:
    def __init__(self):
        self.event_list = []

    def __call__(self, value=0):
        for event in self.event_list:
            if event:
                event(value)

    def add(self, _event: SingleEvent):
        self.event_list.append(_event)
