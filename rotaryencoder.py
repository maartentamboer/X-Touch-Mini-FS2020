import mido
from activelayer import *

class RotaryEncoder:
    def __init__(self, encoder_index, outport: mido.ports.BaseOutput):
        self._encoder_index = encoder_index
        self._receive_data_cc = self._encoder_index
        self._receive_data_note = self._encoder_index - 1
        self._led_ring_value_cc = self._encoder_index + 8
        self._on_layer = ActiveLayerIdentifier.A
        self._event_up = None
        self._event_down = None

        if self._encoder_index > 8:
            self._receive_data_cc += 2
            self._receive_data_note += 15
            self._led_ring_value_cc -= 8
            self._on_layer = ActiveLayerIdentifier.B

        self._outport = outport

    def set_led_ring_value(self, value: int, blink=False):
        if ActiveLayer().active_layer != self._on_layer:
            return
        if blink:
            value += 13
        msg = mido.Message('control_change', control=self._led_ring_value_cc, value=value)
        self._outport.send(msg)

    def set_led_ring_on_off(self, on: bool, blink=False):
        if ActiveLayer().active_layer != self._on_layer:
            return
        value = 0
        if on:
            value = 27
            if blink:
                value = 28
        msg = mido.Message('control_change', control=self._led_ring_value_cc, value=value)
        self._outport.send(msg)

    def bind_to_event(self, event_up, event_down):
        self._event_up = event_up
        self._event_down = event_down

    @property
    def rotary_control_channel(self):
        return self._receive_data_cc

    @property
    def button_note(self):
        return self._receive_data_note

    def on_cc_data(self, value):
        print(f"on_cc_data: {self._encoder_index}: {value}")
        self._update_active_layer()
        times = abs(64 - value)
        if value > 64 and self._event_up:
            for x in range(times):
                self._event_up()
        elif self._event_down:
            for x in range(times):
                self._event_down()


    def on_note_data(self):
        print(f"on_note_data ENC: {self._encoder_index}")
        self._update_active_layer()

    def _update_active_layer(self):
        ActiveLayer().active_layer = self._on_layer
