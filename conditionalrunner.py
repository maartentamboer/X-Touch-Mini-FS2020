from jinja2 import Environment, select_autoescape
from globalstorage import GlobalStorage

from SimConnect import Event
from MSFSPythonSimConnectMobiFlightExtension.src.simconnect_mobiflight import SimConnectMobiFlight
from MSFSPythonSimConnectMobiFlightExtension.src.mobiflight_variable_requests import MobiFlightVariableRequests

env = Environment(
    autoescape=select_autoescape(['html', 'xml'])
)


class ConditionalRunner:
    def __init__(self, template, file=None):
        self._template_str = "".join(template)
        if file:
            with open(f"Configurations/{file}", 'r') as file:
                self._template_str = file.read()
        self._template = env.from_string(self._template_str)
        self._ae = GlobalStorage().aircraft_events
        self._aq = GlobalStorage().aircraft_requests

    def get_simvar_value(self, name: str):
        value = self._aq.get(name)
        return value

    def get_mobiflight_value(self, name: str):
        #Add MobiFlight
        value = GlobalStorage().get_mobiflight_variable(name)
        #print(name,value)
        return value

    def set_simvar_value(self, name: str, value):
        self._aq.set(name, value)

    def trigger_event(self, name: str, value):
        event = Event(name.encode(), self._ae.sm)
        event(int(value))

    @staticmethod
    def trigger_encoder_alternate(index: int, value: bool):
        GlobalStorage().encoders[index-1].on_alternate(value)

    @staticmethod
    def set_global_variable(key: str, value):
        GlobalStorage().set_global_variable(key, value)

    @staticmethod
    def get_global_variable(key: str):
        return GlobalStorage().get_global_variable(key)

    @staticmethod
    def print(data):
        print(data)

    @staticmethod
    def set_button_led(index: int, on: bool, blink=False):
        GlobalStorage().buttons[index-1].set_led_on_off(on, blink)

    @staticmethod
    def set_encoder_led(index: int, on: bool, blink=False):
        GlobalStorage().encoders[index-1].set_led_ring_on_off(on, blink)

    @staticmethod
    def set_encoder_led_value(index: int, value: int, blink=False):
        GlobalStorage().encoders[index - 1].set_led_ring_value(int(value), blink)

    def execute(self):
        try:
            self._template.render(data=self)
        except Exception as e:
            print('Exception during execution of template:', e)
            print('For template:', self._template_str)

    def __call__(self, *args, **kwargs):
        self.execute()
