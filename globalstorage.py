from typing import List, Any

from SimConnect import AircraftEvents, AircraftRequests

from singleton import Singleton
from rotaryencoder import RotaryEncoder
from pushbutton import PushButton
from trigger import Trigger
from fader import Fader


class GlobalStorage(metaclass=Singleton):
    def __init__(self):
        self._buttons = []   # type: List[PushButton]
        self._encoders = []  # type: List[RotaryEncoder]
        self._faders = []    # type: List[Fader]
        self._triggers = []  # type: List[Trigger]
        self._ae = None
        self._aq = None
        self._global_variables = {}

    def clear(self):
        self._buttons = []
        self._encoders = []
        self._faders = []
        self._triggers = []

    def add_encoder(self, encoder: RotaryEncoder):
        self._encoders.append(encoder)

    def add_button(self, button: PushButton):
        self._buttons.append(button)

    def add_fader(self, fader: Fader):
        self._faders.append(fader)

    def add_trigger(self, trigger: Trigger):
        self._triggers.append(trigger)

    def set_aircraft_events(self, ae: AircraftEvents):
        self._ae = ae

    def set_aircraft_requests(self, aq: AircraftRequests):
        self._aq = aq

    def set_global_variable(self, key: str, value):
        self._global_variables[key] = value

    def get_global_variable(self, key: str):
        return self._global_variables.get(key, None)

    @property
    def encoders(self) -> List[RotaryEncoder]:
        return self._encoders

    @property
    def buttons(self) -> List[PushButton]:
        return self._buttons

    @property
    def faders(self) -> List[Fader]:
        return self._faders

    @property
    def triggers(self) -> List[Trigger]:
        return self._triggers

    @property
    def all_elements(self) -> List[Any]:
        return self._encoders + self._buttons + self._triggers

    @property
    def aircraft_events(self) -> AircraftEvents:
        return self._ae

    @property
    def aircraft_requests(self) -> AircraftRequests:
        return self._aq
