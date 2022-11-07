from e2sysex import *
from e2_midi import *
from e2_syx_codec import *
import e2_formats as fmt

import logging
from time import sleep


def main():
    logging.basicConfig(level=logging.DEBUG)

    e = E2Sysex()
    fxe = FXEditor()
    
    #fxe.preset = fmt.fx_preset.parse(e.get_ifx(2))
    #fxe.preset.name = 'Editstortion'
    #e.set_ifx(4, fmt.fx_preset.build(fxe.preset))

class FXEditor:
    
    # sysex is E2Sysex() instace
    # preset is fx preset as bytes
    def __init__(self, preset=None):
        logging.debug('Initialise FX Editor')
        #self.midi = midi
        #self.sysex = sysex
        
        if preset is not None:
            logging.debug('Parse initial preset')
            self._preset = fmt.fx_preset.parse(preset)
        else:
            logging.debug('Parse default preset')
            self.preset = fmt.fx_preset.parse(fmt.fx_preset.build({}))

        
    
    

if __name__ == "__main__":
    main()
