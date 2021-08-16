from activelayer import ActiveLayer, ActiveLayerIdentifier


class Fader:
    def __init__(self, fader_index):
        self._fader_index = fader_index
        self._receive_data_cc = self._fader_index + 8  # CC9 and CC10
        self._event = None
        self._on_layer = ActiveLayerIdentifier.A
        self._min_value = 0
        self._max_value = 0

        if self._fader_index > 1:
            self._on_layer = ActiveLayerIdentifier.B

    @property
    def control_channel(self):
        return self._receive_data_cc

    def bind_to_event(self, event, min_value, max_value):
        self._event = event
        self._min_value = min_value
        self._max_value = max_value

    def reset_configuration(self):
        self._event = None
        self._min_value = 0
        self._max_value = 0

    def on_cc_data(self, value):
        print(f"on_cc_data: {self._fader_index}: {value}")
        self._update_active_layer()

        converted = self._map(value, 0, 127, self._min_value, self._max_value)

        if self._event:
            self._event(converted)

    def _update_active_layer(self):
        ActiveLayer().active_layer = self._on_layer

    #  Prominent Arduino map function :)
    @staticmethod
    def _map(x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
