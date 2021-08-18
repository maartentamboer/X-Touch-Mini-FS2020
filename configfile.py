import json

from eventqueue import EventQueue, SingleEvent
from trigger import Trigger
from conditionalrunner import ConditionalRunner
from globalstorage import GlobalStorage
from SimConnect import RequestList
from initialization import Initialization

class ConfigFile:
    def __init__(self, aircraft):
        self._encoders = GlobalStorage().encoders
        self._buttons = GlobalStorage().buttons
        self._faders = GlobalStorage().faders
        self._triggers = GlobalStorage().triggers
        self._ae = GlobalStorage().aircraft_events
        self._aq = GlobalStorage().aircraft_requests
        self._aircraft = aircraft

    def configure(self):
        with open('Configurations/config.json') as base_json_file:
            base_data = json.load(base_json_file)
            config_file = base_data['default']
            for elem in base_data['aircraft']:
                aircraft_contains = elem['aircraft_contains']
                file = elem['file']
                if aircraft_contains in str(self._aircraft):
                    config_file = file
            self._configure_additional_simvars(base_data)
            if 'automatic_layer_revert' in base_data:
                GlobalStorage().active_layer_changer.enable_layer_revert_timer(base_data['automatic_layer_revert'])

            config_file = 'Configurations/' + config_file  # Add folder prefix
            print("Loading config file:", config_file)
            with open(config_file) as json_file:
                data = json.load(json_file)
                self._configure_encoders(data['encoders'])
                self._configure_buttons(data['buttons'])
                self._configure_faders(data['faders'])
                self._configure_triggers(data['triggers'])
                Initialization(data.get('initialization', None))

    @staticmethod
    def get_midi_input() -> str:
        with open('Configurations/config.json') as base_json_file:
            base_data = json.load(base_json_file)
            return base_data.get('midi_input_device', 'X-TOUCH MINI 0')

    @staticmethod
    def get_midi_output() -> str:
        with open('Configurations/config.json') as base_json_file:
            base_data = json.load(base_json_file)
            return base_data.get('midi_output_device', 'X-TOUCH MINI 1')

    @property
    def triggers(self):
        return self._triggers

    def _create_binding(self, obj, events):  # Support multiple events for one binding
        event_queue = EventQueue()

        # Check for multiple events by checking for a list
        if isinstance(events, list):
            for event in events:
                event_queue.add(self._create_single_binding(obj, event))
        else:
            event_queue.add(self._create_single_binding(obj, events))

        return event_queue

    @staticmethod
    def _create_single_binding(obj, event):
        if isinstance(event, str):  # if event is single STRING in JSON: "AP_ALT_VAR_INC"
            if event == "{alternate}":
                return obj.on_alternate_toggle
            return SingleEvent(event)

        event_name = event.get('event')
        event_type = event.get('type')
        event_value = event.get('value', None)
        return SingleEvent(event_name, event_type, event_value)

    def _configure_encoders(self, data):
        for enc in self._encoders:
            enc.reset_configuration()
        for elem in data:
            # print(elem)
            index = elem['index']
            event_up = elem.get('event_up')
            event_down = elem.get('event_down')
            alternate_event_up = elem.get('alternate_event_up')
            alternate_event_down = elem.get('alternate_event_down')
            event_press = elem.get('event_press')
            event_short_press = elem.get('event_short_press')
            event_long_press = elem.get('event_long_press')
            encoder = self._encoders[index - 1]

            if event_up and event_down:
                encoder.bind_to_event(self._create_binding(encoder, event_up),
                                      self._create_binding(encoder, event_down))
            if alternate_event_up and alternate_event_down:
                encoder.bind_to_alternate_event(self._create_binding(encoder, alternate_event_up),
                                                self._create_binding(encoder, alternate_event_down))
            if event_press:
                encoder.bind_press(self._create_binding(encoder, event_press))
            if event_short_press:
                encoder.bind_short_press(self._create_binding(encoder, event_short_press))
            if event_long_press:
                encoder.bind_long_press(self._create_binding(encoder, event_long_press))

    def _configure_buttons(self, data):
        for btn in self._buttons:
            btn.reset_configuration()
        for elem in data:
            # print(elem)
            index = elem['index']
            event_press = elem.get('event_press')
            event_short_press = elem.get('event_short_press')
            event_long_press = elem.get('event_long_press')
            simvar_led = elem.get('simvar_led')
            mobiflightsimvar_led = elem.get('mobiflightsimvar_led')
            button = self._buttons[index - 1]

            if event_press:
                button.bind_press(self._create_binding(button, event_press))
            if event_short_press:
                button.bind_short_press(self._create_binding(button, event_short_press))
            if event_long_press:
                button.bind_long_press(self._create_binding(button, event_long_press))
            if simvar_led:
                button.bind_led_to_simvar(simvar_led)
            if mobiflightsimvar_led:
                button.bind_led_to_mobiflightsimvar(mobiflightsimvar_led)

    def _configure_faders(self, data):
        for fad in self._faders:
            fad.reset_configuration()
        for elem in data:
            # print(elem)
            index = elem['index']
            event_change = elem['event_change']
            min_value = elem['min_value']
            max_value = elem['max_value']

            fader = self._faders[index - 1]
            fader.bind_to_event(self._create_binding(fader, event_change), min_value, max_value)

    def _configure_triggers(self, data):
        for trig in self._triggers:
            trig.reset_configuration()
        self._triggers.clear()
        for elem in data:
            # print(elem)
            simvar = elem.get('simvar')
            trigger_type = elem.get('trigger_type', None)
            trigger_index = elem.get('trigger_index', None)
            condition = elem.get('condition', None)
            object_to_trigger = None
            trigger = Trigger()
            trigger.bind_to_simvar(simvar)

            if trigger_type == "encoder":
                object_to_trigger = self._encoders[trigger_index - 1]
                trigger.bind_to_event(object_to_trigger.on_alternate)
            elif trigger_type == "button":
                object_to_trigger = self._buttons[trigger_index - 1]
            elif trigger_type == "condition":
                trigger.bind_to_event(ConditionalRunner(condition))
            elif trigger_type == "condition-file":
                trigger.bind_to_event(ConditionalRunner("", condition))
            else:
                raise ValueError(f"Unknown trigger type: {trigger_type}")

            self._triggers.append(trigger)

    def _configure_additional_simvars(self, data):
        if 'additional_simvars' in data:
            helper = RequestList.RequestHelper(self._aq.sm)
            helper.list = {}
            for elem in data['additional_simvars']:
                writable = 'N'
                if elem['writable']:
                    writable = 'y'
                simvar_elem = [elem['description'], elem['simvar'].encode(), elem['type'].encode(), writable]
                helper.list[elem['name']] = simvar_elem
            if helper not in self._aq.list:
                self._aq.list.append(helper)
