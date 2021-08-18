import time
import mido
from activelayer import ActiveLayer, ActiveLayerIdentifier


class PushButton:
    def __init__(self, button_index, outport: mido.ports.BaseOutput):
        self._button_index = button_index
        self._receive_data_note = self._button_index + 7
        self._led_control_note = self._button_index - 1
        self._on_layer = ActiveLayerIdentifier.A
        self._simvar = None
        self._mobiflightsimvar = None
        self._event_press = None
        self._event_press_short = None
        self._event_press_long = None
        self._time_of_note_on = time.time()
        self._current_led_value = 0

        if self._button_index > 16:
            self._receive_data_note += 8
            self._led_control_note -= 16
            self._on_layer = ActiveLayerIdentifier.B

        self._outport = outport
        ActiveLayer().subscribe_to_layer_change(self._on_layer_change)

    def set_led_on_off(self, on: bool, blink=False):
        value = 0
        if on:
            value = 1
            if blink:
                value = 2
        self._current_led_value = value

        if ActiveLayer().active_layer == self._on_layer:
            self._update_led()

    def bind_led_to_simvar(self, simvar: str):
        self._simvar = simvar

    def bind_led_to_mobiflightsimvar(self, simvar: str):
        self._mobiflightsimvar = simvar


    def bind_press(self, event):
        self._event_press = event

    def bind_short_press(self, event):
        self._event_press_short = event

    def bind_long_press(self, event):
        self._event_press_long = event

    def reset_configuration(self):
        self._simvar = None
        self._mobiflightsimvar = None
        self._event_press = None
        self._event_press_short = None
        self._event_press_long = None
        self._current_led_value = 0

    @property
    def button_note(self):
        return self._receive_data_note

    @property
    def bound_simvar(self):
        return self._simvar

    @property
    def bound_mobiflightsimvar(self):
        return self._mobiflightsimvar

    def on_note_data(self, on: bool):
        print(f"on_note_data BTN: {self._button_index}")
        self._update_active_layer()
        if on:
            if self._event_press:
                self._event_press()
            self._time_of_note_on = time.time()
        else:
            diff = time.time() - self._time_of_note_on
            if diff > 0.5 and self._event_press_long:
                self._event_press_long()
            elif self._event_press_short:
                self._event_press_short()

    def on_simvar_data(self, data):
        if data == 1.0:
            self.set_led_on_off(True)
        else:
            self.set_led_on_off(False)

    def on_mobiflightsimvar_data(self, data):
        if data == 1.0:
            self.set_led_on_off(True)
        else:
            self.set_led_on_off(False)

    def _update_active_layer(self):
        ActiveLayer().active_layer = self._on_layer

    def _update_led(self):
        msg = mido.Message('note_on', note=self._led_control_note, velocity=self._current_led_value)
        self._outport.send(msg)

    def _on_layer_change(self, newlayer):
        if newlayer == self._on_layer:
            self._update_led()
