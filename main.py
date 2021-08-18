import time
import logging
from SimConnect import AircraftEvents, AircraftRequests
from MSFSPythonSimConnectMobiFlightExtension.src.simconnect_mobiflight import SimConnectMobiFlight
from MSFSPythonSimConnectMobiFlightExtension.src.mobiflight_variable_requests import MobiFlightVariableRequests
from rotaryencoder import RotaryEncoder
from pushbutton import PushButton
from fader import Fader
from configfile import ConfigFile
from globalstorage import GlobalStorage
from mocksimconnect import MockAircraftEvents, MockAircraftRequests
from activelayerchanger import ActiveLayerChanger
from midiconnection import MidiConnection


def connect_to_simulator(offline: bool):
    sm = None
    is_connected = False
    waiting_time = 10
    while not is_connected and not offline:
        try:
            sm = SimConnectMobiFlight()
            is_connected = True
        except Exception:
            print(f"Connection to simulator not possible. Retry in {waiting_time}s.") 
            time.sleep(waiting_time)
    return sm


def initialize(global_storage: GlobalStorage, 
               sm: SimConnectMobiFlight,
               midi_connection: MidiConnection):
    if sm:
        sm = SimConnectMobiFlight()
        vr = MobiFlightVariableRequests(sm)
        vr.clear_sim_variables()
        global_storage.set_aircraft_events(AircraftEvents(sm))
        global_storage.set_aircraft_requests(AircraftRequests(sm, _time=200))
        global_storage.set_mobiflight_variable_requests(vr) # Add MobiFlight
    else:
        global_storage.set_aircraft_events(MockAircraftRequests())
        global_storage.set_aircraft_requests(MockAircraftEvents())

    for e in range(1, 17):
        encoder = RotaryEncoder(e, midi_connection.outport)
        midi_connection.register_encoder(encoder)
        global_storage.add_encoder(encoder)

    for b in range(1, 33):
        btn = PushButton(b, midi_connection.outport)
        midi_connection.register_button(btn)
        global_storage.add_button(btn)

    for f in range(1, 3):
        fader = Fader(f)
        midi_connection.register_fader(fader)
        global_storage.add_fader(fader)

    global_storage.set_active_layer_changer(ActiveLayerChanger(midi_connection.outport))


def run_aircraft_configuration(global_storage: GlobalStorage):
    aq = global_storage.aircraft_requests
    vr = global_storage.mobiflight_variable_requests
    current_aircraft = "None"
    # Main program loop which checks for aircraft change
    # and reads the simvars for loaded configuration
    while True:
        aircraft = aq.get('TITLE')
        if aircraft and aircraft != current_aircraft:
            print("Aircraft changed from", current_aircraft, "to", aircraft)
            current_aircraft = aircraft
            c = ConfigFile(current_aircraft)
            c.configure()

        for obj in global_storage.all_elements:
            if obj.bound_simvar and aq:
                sv = aq.get(obj.bound_simvar)
                obj.on_simvar_data(sv)

            if obj.bound_mobiflightsimvar and vr:
                sv = vr.get(obj.bound_mobiflightsimvar)
                obj.on_mobiflightsimvar_data(sv)
        time.sleep(0.05)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.ERROR)
    is_offline = False
    storage = GlobalStorage()
    midi = MidiConnection()
    try:
        simconnect = connect_to_simulator(is_offline)
        initialize(storage, simconnect, midi)
        run_aircraft_configuration(storage)
    except Exception as ex:
        print(type(ex), ex)
    finally:
        midi.deinit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
