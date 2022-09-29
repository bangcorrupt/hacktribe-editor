from e2sysex import *
from e2_midi import *
from e2_syx_codec import *
import e2_formats as fmt

import logging
from time import sleep

def midi_input_handler(msg):
    logging.debug('Called input_handler')
    logging.info('MIDI received ' + str(msg))
    
    # SysEx handled by E2Sysex
    if msg.type == 'sysex':
        pass
    
    elif msg.type == 'note_on':
        self.outport.send(msg) # pass note input to output
    
    elif msg.type == 'control_change':
        if msg.control in self.nrpn_cc_map:
            self.map_cc_nrpn(msg)           # map cc to nrpn
        else:
            pass                            # ADD - cc remap



def main():
    logging.basicConfig(level=logging.DEBUG)
  
    m = E2Midi(inport=mido.open_input('MPK mini 3:MPK mini 3 MIDI 1'))
    e = E2Sysex()
    fxe = E2FXEditor(m, e)

    #m.inport.callback = midi_input_handler

    fxe.get_preset(2)
    
    print(fxe.preset.name)
    
    fxe.preset.name = 'Editstortion'
    
    #fxe.set_preset(1)

    print(fxe.preset.name)

    #fxe.midi.run_live()
    
    #sleep(10)
    
    #fxe.midi.run = False
    
    input('Press ENTER to exit') 

    # keepalive
    #while True:
    #    sleep(100)

class E2FXEditor:
    
    # sysex is E2Sysex() instace
    # preset is fx preset as bytes
    def __init__(self, midi, sysex, preset=None):
        logging.debug('Initialise FX Editor')
        self.midi = midi
        self.sysex = sysex

        #msg = mido.Message('note_on', note=64)
        #self.midi.outport.send(msg)
        
        if preset is not None:
            logging.debug('Parse initial preset')
            self._preset = fmt.fx_preset.parse(preset)
        else:
            logging.debug('Parse default preset')
            self.preset = fmt.fx_preset.parse(fmt.fx_preset.build({}))
        


    def get_preset(self, idx, mfx=False):
        if mfx == False:
            logging.debug('Get IFX Preset: ' + str(idx))
            self.preset = fmt.fx_preset.parse(
                                        bytes(self.sysex.get_ifx(idx)))
        elif mfx == True:
            logging.warning('MFX not implemented yet')
            
    
    def set_preset(self, idx, mfx=False):
        if mfx == False:
            logging.debug('Set IFX Preset: ' + str(idx))
            self.sysex.set_ifx(idx, fmt.fx_preset.build(self.preset))
        
        elif mfx == True:
            logging.warning('MFX not implemented yet')
    
    

if __name__ == "__main__":
    main()
