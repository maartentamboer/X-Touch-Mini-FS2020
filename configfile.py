import json
from typing import List
from functools import partial

from SimConnect import AircraftEvents

from eventqueue import *

from pushbutton import *
from rotaryencoder import *
from trigger import *
from fader import *


class ConfigFile:
    def __init__(self, encoders: List[RotaryEncoder], buttons: List[PushButton], faders: List[Fader], ae: AircraftEvents):
        self._encoders = encoders
        self._buttons = buttons
        self._faders = faders
        self._triggers = []
        self._ae = ae

    def configure(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            self._configure_encoders(data['encoders'])
            self._configure_buttons(data['buttons'])
            self._configure_faders(data['faders'])
            self._configure_triggers(data['triggers'])

    @property
    def triggers(self):
        return self._triggers

    def _mock_binding(self, msg: str):
        print(f"{msg}")

    def _mock_binding(self, msg: str, value):
        print(f"{msg} to {value}")

    def _create_binding(self, obj, events): #Support multiple events for one binding 
        event_queue = EventQueue()

        if isinstance(events, list):
            for event in events:
                event_queue.add(self._create_single_binding(obj, event))
        else:
            event_queue.add(self._create_single_binding(obj, events))

        return event_queue

    def _create_single_binding(self, obj, event):
        if (isinstance(event, str)): #if event is single STRING in JSON
            event_name = event
            event_type = "auto"
            event_value = "0"
            event_description = ""
        else: #if event is complex type {"event": "ALTITUDE_SLOT_INDEX_SET", "type": "manual", "value": 1, "description": "A32NX - set AP Altitude Hold to selected mode"},
            event_name = event.get('event')
            event_type = event.get('type')
            event_value = event.get('value')
            event_description = event.get('description')

        if self._ae:
            if event_name:
                return SingleEvent(self._ae, event_name, event_type, event_value, event_description)
            elif event == "{alternate}":
                return obj.on_alternate_toggle            
            else:
                return SingleEvent(self._ae, event)
        else:
            return partial(self._mock_binding, event)
 
    def _configure_encoders(self, data):
        for elem in data:
            print(elem)
            index = elem['index']
            event_up = elem.get('event_up')
            event_down = elem.get('event_down')
            alternate_event_up = elem.get('alternate_event_up')
            alternate_event_down = elem.get('alternate_event_down')
            event_press = elem.get('event_press')
            event_short_press = elem.get('event_short_press')
            event_long_press = elem.get('event_long_press')
            encoder = self._encoders[index - 1]

            if event_up and event_down:
                encoder.bind_to_event(self._create_binding(encoder, event_up),
                                      self._create_binding(encoder, event_down))
            if alternate_event_up and alternate_event_down:
                encoder.bind_to_alternate_event(self._create_binding(encoder, alternate_event_up),
                                                self._create_binding(encoder, alternate_event_down))
            if event_press:
                encoder.bind_press(self._create_binding(encoder, event_press))
            if event_short_press:
                encoder.bind_short_press(self._create_binding(encoder, event_short_press))
            if event_long_press:
                encoder.bind_long_press(self._create_binding(encoder, event_long_press))

    def _configure_buttons(self, data):
        for elem in data:
            print(elem)
            index = elem['index']
            event_press = elem.get('event_press')
            event_short_press = elem.get('event_short_press')
            event_long_press = elem.get('event_long_press')
            simvar_led = elem.get('simvar_led')
            button = self._buttons[index - 1]

            if event_press:
                button.bind_press(self._create_binding(button, event_press))
            if event_short_press:
                button.bind_short_press(self._create_binding(button, event_short_press))
            if event_long_press:
                button.bind_long_press(self._create_binding(button, event_long_press))
            if simvar_led:
                button.bind_led_to_simvar(simvar_led)

    def _configure_faders(self, data):
        for elem in data:
            print(elem)
            index = elem['index']
            event_change = elem['event_change']
            min_value = elem['min_value']
            max_value = elem['max_value']

            fader = self._faders[index - 1]
            fader.bind_to_event(self._create_binding(fader, event_change), min_value, max_value)

    def _configure_triggers(self, data):
        for elem in data:
            print(elem)
            simvar = elem.get('simvar')
            trigger_type = elem.get('trigger_type')
            trigger_index = elem.get('trigger_index')
            object_to_trigger = None
            t = Trigger()

            if trigger_type == "encoder":
                object_to_trigger = self._encoders[trigger_index - 1]
            elif trigger_type == "button":
                object_to_trigger = self._buttons[trigger_index - 1]
            else:
                raise ValueError(f"Unknown trigger type: {trigger_type}")

            t.bind_to_simvar(simvar)
            t.bind_to_event(object_to_trigger.on_alternate)

            self._triggers.append(t)
