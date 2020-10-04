import json
from typing import List
from functools import partial

from SimConnect import AircraftEvents

from pushbutton import *
from rotaryencoder import *
from trigger import *


class ConfigFile:
    def __init__(self, encoders: List[RotaryEncoder], buttons: List[PushButton], ae: AircraftEvents):
        self._encoders = encoders
        self._buttons = buttons
        self._triggers = []
        self._ae = ae

    def configure(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            self._configure_encoders(data['encoders'])
            self._configure_buttons(data['buttons'])
            self._configure_triggers(data['triggers'])

    @property
    def triggers(self):
        return self._triggers

    def _mock_binding(self, msg: str):
        print(f"{msg}")

    def _create_binding(self, obj, event: str):
        if event == "{alternate}":
            return obj.on_alternate_toggle
        if self._ae:
            return self._ae.find(event)
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
