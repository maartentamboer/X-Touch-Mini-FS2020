
class Trigger:
    def __init__(self):
        self._simvar = None
        self._event = None
        self._previous_data = None

    def bind_to_simvar(self, simvar: str):
        self._simvar = simvar

    def bind_to_event(self, event):
        self._event = event

    def reset_configuration(self):
        self._simvar = None
        self._event = None
        self._previous_data = None

    @property
    def bound_simvar(self):
        return self._simvar

    @property
    def bound_mobiflightsimvar(self):
        return None

    def on_simvar_data(self, data):
        # Check if data has changed this prevents unnecessary execution of events
        if data != self._previous_data:
            self._previous_data = data
            if self._event:
                if data == 1.0:
                    self._event(True)
                else:
                    self._event(False)
