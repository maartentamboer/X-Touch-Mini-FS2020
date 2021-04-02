from threading import Timer
import mido
import time

from singleton import Singleton
from activelayer import ActiveLayer, ActiveLayerIdentifier


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class ActiveLayerChanger:
    def __init__(self, outport: mido.ports.BaseOutput):
        self._timer = None
        self._layer_revert_interval = 0.0
        self._outport = outport
        self._time_of_last_activity = time.time()
        ActiveLayer().subscribe_to_layer_change(self._on_layer_change)
        ActiveLayer().subscribe_to_activity(self._on_activity)

    def set_active_layer(self, newlayer: ActiveLayerIdentifier):
        if newlayer == ActiveLayerIdentifier.A:
            msg = mido.Message('program_change', program=0)
        else:
            msg = mido.Message('program_change', program=1)
        self._outport.send(msg)
        ActiveLayer().active_layer = newlayer

    def enable_layer_revert_timer(self, interval: float):
        self._time_of_last_activity = time.time()
        self._timer = RepeatedTimer(0.1, self._layer_revert_timer_event)
        self._layer_revert_interval = interval

    def _on_layer_change(self, newlayer):
        if self._timer:
            if newlayer == ActiveLayerIdentifier.B:
                self._timer.start()
            else:
                self._timer.stop()

    def _on_activity(self, layer):
        self._time_of_last_activity = time.time()

    def _layer_revert_timer_event(self):
        current_time = time.time()
        if current_time - self._time_of_last_activity > self._layer_revert_interval:
            print("Automatic change to layer A")
            self.set_active_layer(ActiveLayerIdentifier.A)
