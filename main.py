# This is a sample Python script.
import mido
import time
from SimConnect import *
from rotaryencoder import *
from pushbutton import *
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def print_message(message):
    print(message)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print(mido.get_input_names())
    print(mido.get_output_names())

    outport = mido.open_output('X-TOUCH MINI 1')
    inport = mido.open_input('X-TOUCH MINI 0', callback=print_message)

    for z in range(0, 1):
        for x in range(0, 14):
            for c in range(9, 17):
                msg = mido.Message('control_change', control=c, value=x)
                outport.send(msg)
            time.sleep(0.05)
    for c in range(9, 17):
        msg = mido.Message('control_change', control=c, value=28)
        outport.send(msg)

    for c in range(0, 17):
        msg = mido.Message('note_on', note=c, velocity=1)
        outport.send(msg)
        time.sleep(0.05)

    for c in range(0, 17):
        msg = mido.Message('note_on', note=c, velocity=0)
        outport.send(msg)
        time.sleep(0.05)

    while True:
        pass


def simconnect_test():
    sm = SimConnect()
    aq = AircraftRequests(sm, _time=200)
    ae = AircraftEvents(sm)
    event_to_trigger = ae.find("TOGGLE_FLIGHT_DIRECTOR")
    hdg_inc = ae.find('HEADING_BUG_INC')
    hdg_dec = ae.find('HEADING_BUG_DEC')
    vs_inc = ae.find('AP_VS_VAR_INC')
    vs_dec = ae.find('AP_VS_VAR_DEC')
    spd_inc = ae.find('AP_SPD_VAR_INC')
    spd_dec = ae.find('AP_SPD_VAR_DEC')
    vs_active = False

    def handle_message(msg: mido.Message):
        print(msg)

        if msg.type == 'note_on' and msg.note == 9:
            event_to_trigger()
        elif msg.type == 'control_change' and msg.control == 3:
            times = abs(64 - msg.value)
            if msg.value > 64:
                for x in range(times):
                    if vs_active:
                        vs_inc()
                    else:
                        spd_inc()
            else:
                for x in range(times):
                    if vs_active:
                        vs_dec()
                    else:
                        spd_dec()

    outport = mido.open_output('X-TOUCH MINI 1')
    inport = mido.open_input('X-TOUCH MINI 0', callback=handle_message)

    while True:
        ap = aq.get('AUTOPILOT_FLIGHT_DIRECTOR_ACTIVE')
        vs = aq.get('AUTOPILOT_VERTICAL_HOLD')
        if ap == 1:
            msg = mido.Message('note_on', note=1, velocity=1)
        else:
            msg = mido.Message('note_off', note=1, velocity=0)
        if vs == 1:
            msg = mido.Message('note_on', note=2, velocity=1)
            vs_active = True
        else:
            msg = mido.Message('note_off', note=2, velocity=0)
            vs_active = False
        outport.send(msg)
        time.sleep(0.1)

def midi_test():
    sm = SimConnect()
    aq = AircraftRequests(sm, _time=200)
    ae = AircraftEvents(sm)

    outport = mido.open_output('X-TOUCH MINI 1')
    control_change_dict = {}
    note_dict = {}

    def handle_message(msg: mido.Message):
        print(msg)
        if msg.type == 'control_change':
            if msg.control in control_change_dict:
                control_change_dict[msg.control].on_cc_data(msg.value)
        elif msg.type == 'note_on':
            if msg.note in note_dict:
                note_dict[msg.note].on_note_data()

    inport = mido.open_input('X-TOUCH MINI 0', callback=handle_message)

    encoder = RotaryEncoder(1, outport)
    encoder.bind_to_event(ae.find('HEADING_BUG_INC'),
                          ae.find('HEADING_BUG_DEC'))

    btn = PushButton(1, outport)
    btn.bind_led_to_simvar('AUTOPILOT_FLIGHT_DIRECTOR_ACTIVE')
    btn.bind_to_event(ae.find('TOGGLE_FLIGHT_DIRECTOR'))

    encs = []
    for e in range(1, 17):
        print(e)
        encoder = RotaryEncoder(e, outport)
        if e == 1:
            encoder.bind_to_event(ae.find('HEADING_BUG_INC'),
                                  ae.find('HEADING_BUG_DEC'))
        control_change_dict[encoder.rotary_control_channel] = encoder
        note_dict[encoder.button_note] = encoder
        encs.append(encoder)

    btns = []
    for b in range(1, 33):
        print(b)
        btn = PushButton(b, outport)
        if b == 1:
            btn.bind_led_to_simvar('AUTOPILOT_FLIGHT_DIRECTOR_ACTIVE')
            btn.bind_to_event(ae.find('TOGGLE_FLIGHT_DIRECTOR'))
        if b == 2:
            btn.bind_led_to_simvar('AUTOPILOT_YAW_DAMPER')
            btn.bind_to_event(ae.find('YAW_DAMPER_TOGGLE'))
        note_dict[btn.button_note] = btn
        btns.append(btn)

    while True:
        for btn in btns:
            if btn.bound_simvar:
                sv = aq.get(btn.bound_simvar)
                btn.on_simvar_data(sv)
        time.sleep(0.1)
        # for val in [True, False]:
        #     for x in range(8):
        #         encs[x].set_led_ring_on_off(val)
        #         time.sleep(0.05)
        #     for x in range(16):
        #         btns[x].set_led_on_off(val, False)
        #         time.sleep(0.05)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # simconnect_test()
    # midi_test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
