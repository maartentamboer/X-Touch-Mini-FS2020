import time

import mido

from SimConnect import SimConnect, AircraftEvents, AircraftRequests
from SimConnectMobiflight.simconnect_mobiflight import SimConnectMobiFlight
from SimConnectMobiflight.mobiflight_variable_requests import MobiFlightVariableRequests
from rotaryencoder import RotaryEncoder
from pushbutton import PushButton
from fader import Fader
from configfile import ConfigFile
from globalstorage import GlobalStorage
from mocksimconnect import MockAircraftEvents, MockAircraftRequests
from activelayerchanger import ActiveLayerChanger
from activelayer import ActiveLayer


def main_app(offline: bool):
    global_storage = GlobalStorage()
    sm = None
    vr = None
    aq = None
    ae = None
    if not offline:
        sm = SimConnectMobiFlight()
        vr = MobiFlightVariableRequests(sm)
        vr.clear_sim_variables()
        aq = AircraftRequests(sm, _time=200)
        ae = AircraftEvents(sm)
        global_storage.set_aircraft_events(ae)
        global_storage.set_aircraft_requests(aq)
        #Add MobiFlight
        global_storage.set_mobiflightvariablerequests(vr)

    else:
        aq = MockAircraftRequests()
        ae = MockAircraftEvents()
        global_storage.set_aircraft_events(MockAircraftEvents())
        global_storage.set_aircraft_requests(MockAircraftRequests())

    ActiveLayer().clear_all_subscriptions()

    print('Midi input devices:', mido.get_input_names())
    print('Midi output devices:', mido.get_output_names())
    selected_input = ConfigFile.get_midi_input()
    selected_output = ConfigFile.get_midi_output()
    print('Using midi input device:', selected_input)
    print('Using midi output device:', selected_output)

    aircraft = aq.get('TITLE')
    print("Current aircraft:", aircraft)
    outport = mido.open_output(selected_output)  # pylint: disable=no-member

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

    inport = mido.open_input(selected_input, callback=handle_message)  # pylint: disable=no-member

    for e in range(1, 17):
        encoder = RotaryEncoder(e, outport)
        global_storage.add_encoder(encoder)

    for b in range(1, 33):
        btn = PushButton(b, outport)
        global_storage.add_button(btn)

    for f in range(1, 3):
        fader = Fader(f)
        global_storage.add_fader(fader)

    GlobalStorage().set_active_layer_changer(ActiveLayerChanger(outport))

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

    while True:
        for obj in GlobalStorage().all_elements:
            if obj.bound_simvar and aq:
                sv = aq.get(obj.bound_simvar)
                obj.on_simvar_data(sv)

            if obj.bound_mobiflightsimvar and vr:
                sv = vr.get(obj.bound_mobiflightsimvar)
                obj.on_mobiflightsimvar_data(sv)

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
