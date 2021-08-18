import time
import mido
from activelayer import ActiveLayer, ActiveLayerIdentifier


class RotaryEncoder:
    def __init__(self, encoder_index, outport: mido.ports.BaseOutput):
        self._encoder_index = encoder_index
        self._receive_data_cc = self._encoder_index
        self._receive_data_note = self._encoder_index - 1
        self._led_ring_value_cc = self._encoder_index + 8
        self._on_layer = ActiveLayerIdentifier.A
        self._event_up = None
        self._event_down = None
        self._alternate_event_up = None
        self._alternate_event_down = None
        self._alternate_active = False
        self._event_press = None
        self._event_press_short = None
        self._event_press_long = None
        self._time_of_note_on = time.time()
        self._current_led_ring_value = 0

        if self._encoder_index > 8:
            self._receive_data_cc += 2
            self._receive_data_note += 16
            self._led_ring_value_cc -= 8
            self._on_layer = ActiveLayerIdentifier.B

        self._outport = outport
        ActiveLayer().subscribe_to_layer_change(self._on_layer_change)

    def set_led_ring_value(self, value: int, blink=False):
        if blink:
            value += 13
        self._current_led_ring_value = value

        if ActiveLayer().active_layer == self._on_layer:
            self._update_led_ring()

    def set_led_ring_on_off(self, on: bool, blink=False):
        if ActiveLayer().active_layer != self._on_layer:
            return
        value = 0
        if on:
            value = 27
            if blink:
                value = 28
        self._current_led_ring_value = value
        self._update_led_ring()

    def bind_to_event(self, event_up, event_down):
        self._event_up = event_up
        self._event_down = event_down

    def bind_to_alternate_event(self, event_up, event_down):
        self._alternate_event_up = event_up
        self._alternate_event_down = event_down

    def bind_press(self, event):
        self._event_press = event

    def bind_short_press(self, event):
        self._event_press_short = event

    def bind_long_press(self, event):
        self._event_press_long = event

    def reset_configuration(self):
        self._event_up = None
        self._event_down = None
        self._alternate_event_up = None
        self._alternate_event_down = None
        self._alternate_active = False
        self._event_press = None
        self._event_press_short = None
        self._event_press_long = None
        self._current_led_ring_value = 0

    @property
    def rotary_control_channel(self):
        return self._receive_data_cc

    @property
    def button_note(self):
        return self._receive_data_note

    @property
    def bound_simvar(self):
        return None

    @property
    def bound_mobiflightsimvar(self):
        return None


    def on_cc_data(self, value):
        print(f"on_cc_data: {self._encoder_index}: {value}")
        self._update_led_ring()
        self._update_active_layer()
        times = abs(64 - value)
        up_event = self._event_up
        down_event = self._event_down
        if times > 10:
            print("Either you're turning really fast, or encoder", self._encoder_index, "is not in relative 2 mode")
        if self._alternate_active:
            up_event = self._alternate_event_up
            down_event = self._alternate_event_down

        if value > 64 and up_event:
            for _ in range(times):
                up_event()
        elif down_event:
            for _ in range(times):
                down_event()

    def on_note_data(self, on: bool):
        print(f"on_note_data ENC: {self._encoder_index}: {on}")
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

    def on_alternate(self, enable: bool):
        self._alternate_active = enable

    def on_alternate_toggle(self, _):
        self._alternate_active = not self._alternate_active

    def _update_active_layer(self):
        ActiveLayer().active_layer = self._on_layer

    def _update_led_ring(self):
        msg = mido.Message('control_change', control=self._led_ring_value_cc, value=self._current_led_ring_value)
        self._outport.send(msg)

    def _on_layer_change(self, newlayer):
        if newlayer == self._on_layer:
            self._update_led_ring()
