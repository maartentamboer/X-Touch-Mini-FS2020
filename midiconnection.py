import mido
import time
from configfile import ConfigFile

class MidiConnection:
    def __init__(self):
        print('Midi input devices:', mido.get_input_names())
        print('Midi output devices:', mido.get_output_names())
        selected_input = ConfigFile.get_midi_input()
        selected_output = ConfigFile.get_midi_output()
        print('Using midi input device:', selected_input)
        print('Using midi output device:', selected_output) 
        self._control_change_dict = {}
        self._note_dict = {}
        is_connected = False
        waiting_time = 3
        while not is_connected :
            try:    
                self._outport = mido.open_output(selected_output)  # pylint: disable=no-member
                self._inport = mido.open_input(selected_input, callback=self.handle_message)  # pylint: disable=no-member
                is_connected = True
            except Exception:
                print(f"Connection to X-Touch-Mini not possible. Connected? Retry in {waiting_time}s.") 
                time.sleep(waiting_time)


    def handle_message(self, msg: mido.Message):
        # print(msg)
        if msg.type == 'control_change':
            if msg.control in self._control_change_dict:
                self._control_change_dict[msg.control].on_cc_data(msg.value)
        elif msg.type == 'note_on':
            if msg.note in self._note_dict:
                self._note_dict[msg.note].on_note_data(True)
        elif msg.type == 'note_off':
            if msg.note in self._note_dict:
                self._note_dict[msg.note].on_note_data(False)

    def register_button(self, btn):
        self._note_dict[btn.button_note] = btn

    def register_encoder(self, encoder):
        self._control_change_dict[encoder.rotary_control_channel] = encoder
        self._note_dict[encoder.button_note] = encoder

    def register_fader(self, fader):
        self._control_change_dict[fader.control_channel] = fader

    def deinit(self):
        self._outport.close()
        self._inport.close()

    @property
    def outport(self):
        return self._outport
    
    @property
    def inport(self):
        return self._inport
