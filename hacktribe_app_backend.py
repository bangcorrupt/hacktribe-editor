from firmware_patcher import FirmwarePatcher
from fx_editor import FXEditor

from e2sysex import *
from e2_midi import *

from pathlib import Path
import logging

def main():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    be = HacktribeAppBackend()
    be.welcome_msg()

# ADD - groove edit, fx edit, pattern edit, etc...
class HacktribeAppBackend:
    def __init__(self):   
        logging.debug('Initialising Backend')

        self.fw_patcher = FirmwarePatcher()
        
        self.midi = E2Midi()        
        self.sysex = E2Sysex()
        
        self.fx_editor = FXEditor(self.midi, self.sysex)

    def welcome_msg(self):
        logging.debug('Display welcome message')
        logging.info('Hacktribe Editor\n')
        logging.info('https://github.com/bangcorrupt/hacktribe\n')


      
if __name__ == "__main__":
    main()
