
from jinja2 import Environment, PackageLoader, select_autoescape
from SimConnect import AircraftRequests, AircraftEvents

env = Environment(
    autoescape=select_autoescape(['html', 'xml'])
)

class ConditionalTrigger:
    def __init__(self, template, ae: AircraftEvents, aq: AircraftRequests):
        template_str = "".join(template)
        self._template = env.from_string(template_str)
        self._ae = ae
        self._aq = aq

    def get_simvar_value(self, name: str):
        value = self._aq.get(name)
        print("get_simvar_value", name, value)
        return value

    def set_simvar_value(self, name: str, value):
        print("set_simvar_value", name, value)
        self._aq.set(name, value)

    def trigger_event(self, name: str, value):
        print("trigger_event", name, value)
        self._ae.find(name)(int(value))

    def trigger_encoder_alternate(self, index: int, value: bool):
        print("trigger_encoder_alternate", index, value)

    def execute(self):
        self._template.render(data=self)

    def __call__(self, *args, **kwargs):
        self.execute()