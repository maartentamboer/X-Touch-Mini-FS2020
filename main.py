import time

import mido

from SimConnect import SimConnect, AircraftEvents, AircraftRequests
from rotaryencoder import RotaryEncoder
from pushbutton import PushButton
from fader import Fader
from configfile import ConfigFile
from globalstorage import GlobalStorage
from mocksimconnect import MockAircraftEvents, MockAircraftRequests


def main_app(offline: bool):
    global_storage = GlobalStorage()
    sm = None
    aq = None
    ae = None
    if not offline:
        sm = SimConnect()
        aq = AircraftRequests(sm, _time=200)
        ae = AircraftEvents(sm)
        global_storage.set_aircraft_events(ae)
        global_storage.set_aircraft_requests(aq)
    else:
        global_storage.set_aircraft_events(MockAircraftEvents())
        global_storage.set_aircraft_requests(MockAircraftRequests())

    aircraft = aq.get('TITLE')
    print("Current aircraft:", aircraft)
    outport = mido.open_output('X-TOUCH MINI 1')  # pylint: disable=no-member

    control_change_dict = {}
    note_dict = {}

    def handle_message(msg: mido.Message):
        # print(msg)
        if msg.type == 'control_change':
            if msg.control in control_change_dict:
                control_change_dict[msg.control].on_cc_data(msg.value)
        elif msg.type == 'note_on':
            if msg.note in note_dict:
                note_dict[msg.note].on_note_data(True)
        elif msg.type == 'note_off':
            if msg.note in note_dict:
                note_dict[msg.note].on_note_data(False)

    inport = mido.open_input('X-TOUCH MINI 0', callback=handle_message)  # pylint: disable=no-member

    for e in range(1, 17):
        encoder = RotaryEncoder(e, outport)
        global_storage.add_encoder(encoder)

    for b in range(1, 33):
        btn = PushButton(b, outport)
        global_storage.add_button(btn)

    for f in range(1, 3):
        fader = Fader(f)
        global_storage.add_fader(fader)

    c = ConfigFile(aircraft)
    c.configure()
    triggers = c.triggers

    for encoder in GlobalStorage().encoders:
        control_change_dict[encoder.rotary_control_channel] = encoder
        note_dict[encoder.button_note] = encoder

    for btn in GlobalStorage().buttons:
        note_dict[btn.button_note] = btn

    for f in GlobalStorage().faders:
        control_change_dict[f.control_channel] = f

    triggers[0].on_simvar_data(1.0)
    count = 0
    while True:
        for obj in GlobalStorage().all_elements:
            if obj.bound_simvar and aq:
                sv = aq.get(obj.bound_simvar)
                obj.on_simvar_data(sv)

        current_aircraft = aq.get('TITLE')
        if current_aircraft and aircraft != current_aircraft:
            print("Aircraft changed from", aircraft, "to", current_aircraft)
            break
        time.sleep(0.05)

    global_storage.clear()
    inport.close()
    outport.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    # simconnect_test()
    # midi_test()
    while True:
        main_app(False)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
