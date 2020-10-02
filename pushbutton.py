import mido
from activelayer import *

class PushButton:
    def __init__(self, button_index, outport: mido.ports.BaseOutput):
        self._button_index = button_index
        self._receive_data_note = self._button_index + 7
        self._led_control_note = self._button_index - 1
        self._on_layer = ActiveLayerIdentifier.A
        self._simvar = None
        self._event = None

        if self._button_index > 16:
            self._receive_data_note += 8
            self._led_control_note -= 15
            self._on_layer = ActiveLayerIdentifier.B

        self._outport = outport

    def set_led_on_off(self, on: bool, blink=False):
        if ActiveLayer().active_layer != self._on_layer:
            return
        value = 0
        if on:
            value = 1
            if blink:
                value = 2
        msg = mido.Message('note_on', note=self._led_control_note, velocity=value)
        self._outport.send(msg)

    def bind_led_to_simvar(self, simvar: str):
        self._simvar = simvar

    def bind_to_event(self, event):
        self._event = event

    @property
    def button_note(self):
        return self._receive_data_note

    @property
    def bound_simvar(self):
        return self._simvar

    def on_note_data(self):
        print(f"on_note_data BTN: {self._button_index}")
        self._update_active_layer()
        if self._event:
            self._event()

    def on_simvar_data(self, data):
        if data == 1.0:
            self.set_led_on_off(True)
        else:
            self.set_led_on_off(False)

    def _update_active_layer(self):
        ActiveLayer().active_layer = self._on_layer
