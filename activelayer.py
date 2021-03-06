from enum import Enum

from singleton import Singleton


class ActiveLayerIdentifier(Enum):
    A = 0
    B = 1


class ActiveLayer(metaclass=Singleton):
    def __init__(self):
        self._active_layer = ActiveLayerIdentifier.A
        self._layer_change_events = []
        self._activity_events = []

    @property
    def active_layer(self):
        return self._active_layer

    @active_layer.setter
    def active_layer(self, value: ActiveLayerIdentifier):
        for x in self._activity_events:
            x(value)
        if value != self._active_layer:
            print("Layer Change to", value)
            for x in self._layer_change_events:
                x(value)
        self._active_layer = value

    def subscribe_to_layer_change(self, callback):
        self._layer_change_events.append(callback)

    def subscribe_to_activity(self, callback):
        self._activity_events.append(callback)

    def clear_all_subscriptions(self):
        self._layer_change_events.clear()
        self._activity_events.clear()
