from enum import Enum

from singleton import Singleton


class ActiveLayerIdentifier(Enum):
    A = 0
    B = 1


class ActiveLayer(metaclass=Singleton):
    def __init__(self):
        self._active_layer = ActiveLayerIdentifier.A

    @property
    def active_layer(self):
        return self._active_layer

    @active_layer.setter
    def active_layer(self, value: ActiveLayerIdentifier):
        self._active_layer = value
