import mido
import logging
from e2sysex import *



def main():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    
    print(mido.get_ioport_names())
    
    m = E2Midi()


# MIDI interface
class E2Midi:
    
    NRPN_MSB_FX_EDIT = 0X01

    nrpn_cc_map = { 0x46:[NRPN_MSB_FX_EDIT, 0, 0],
                    0x47:[NRPN_MSB_FX_EDIT, 0, 1], 
                    0x48:[NRPN_MSB_FX_EDIT, 0, 2], 
                    0x49:[NRPN_MSB_FX_EDIT, 0, 3], 
                    0x4a:[NRPN_MSB_FX_EDIT, 0, 4], 
                    0x4b:[NRPN_MSB_FX_EDIT, 0, 5], 
                    0x4c:[NRPN_MSB_FX_EDIT, 0, 6], 
                    0x4d:[NRPN_MSB_FX_EDIT, 0, 7], 
                    0x4e:[NRPN_MSB_FX_EDIT, 0, 8], 
                    0x4f:[NRPN_MSB_FX_EDIT, 0, 9],
                    0x50:[NRPN_MSB_FX_EDIT, 0, 10], 
                    0x51:[NRPN_MSB_FX_EDIT, 0, 11], 
                    0x52:[NRPN_MSB_FX_EDIT, 0, 12], 
                    0x53:[NRPN_MSB_FX_EDIT, 0, 13], 
                    0x54:[NRPN_MSB_FX_EDIT, 0, 14], 
                    0x55:[NRPN_MSB_FX_EDIT, 0, 15], 
                    0x56:[NRPN_MSB_FX_EDIT, 0, 16], 
                    0x57:[NRPN_MSB_FX_EDIT, 0, 17], 
                    0x58:[NRPN_MSB_FX_EDIT, 0, 18], 
                    0x59:[NRPN_MSB_FX_EDIT, 0, 19], 
                    0x5a:[NRPN_MSB_FX_EDIT, 0, 20], 
                    0x5b:[NRPN_MSB_FX_EDIT, 0, 21], 
                    0x5c:[NRPN_MSB_FX_EDIT, 0, 22], 
                    0x5d:[NRPN_MSB_FX_EDIT, 0, 23], 
                    }


    def __init__(self, inport=None, outport=None, input_handler=None):
        logging.debug('Initialise MIDI')
        
        if inport is not None:
            self.inport = inport
        else:
            self.inport = mido.open_input('electribe2 sampler electribe2 s')
        
        if outport is not None:
            self.outport = outport
        else:
            self.outport = mido.open_output('electribe2 sampler electribe2 s')
        
        if input_handler is not None:
            self.inport.callback = input_handler
        else:
            self.inport.callback=self.input_handler

        
        self.nrpn_cc_map = E2Midi.nrpn_cc_map
        self.fx_chain_idx = 0

    
    def input_handler(self, msg):
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
                self.outport.send(msg)
                pass                            # ADD - cc remap



    def map_cc_nrpn(self, msg):
        logging.debug('Called nrpn_cc_map')
        cc = msg.control
        
        nrpn_msb = self.nrpn_cc_map[cc][0]                          # NRPN-Cat
        
        if nrpn_msb == E2Midi.NRPN_MSB_FX_EDIT: 
            #nrpn_lsb = (msg.channel-1) * 2  + self.nrpn_cc_map[cc][1]   # FX-Slot == part_idx*2 + chain_idx
            if self.fx_chain_idx < 2:
                nrpn_lsb = (msg.channel-1) * 2  + self.fx_chain_idx  # FX-Slot == part_idx*2 + chain_idx
            elif self.fx_chain_idx == 2:
                nrpn_lsb = 0x20
            else:
                logging.debug('FX chain index not found: ' + str(self.fx_chain_idx))
                return
        
        else:
            logging.debug('NRPN category not found: ' + str(nprn_msb))
            return
        
        data_msb = self.nrpn_cc_map[cc][2]                          # fx parameter index
        data_lsb = msg.value                                        # fx parameter value
        
        nrpn = [nrpn_msb, nrpn_lsb, data_msb, data_lsb]
        
        self.send_nrpn(nrpn)
        return
    
    # nrpn is list of nrpn values [nprn-msb, nrpn-lsb, data-msb, data,-lsb]
    def send_nrpn(self, nrpn):
        print('type(nrpn) = ' + str(type(nrpn)))
        msgs =  []
        msgs.append(mido.Message('control_change', control=0x63, value=nrpn[0]))
        msgs.append(mido.Message('control_change', control=0x62, value=nrpn[1]))
        msgs.append(mido.Message('control_change', control=0x06, value=nrpn[2]))
        msgs.append(mido.Message('control_change', control=0x26, value=nrpn[3]))

        for msg in msgs:
            logging.debug('Sending MIDI:' + str(msg))
            self.outport.send(msg)
        
        

if __name__ == '__main__':
    main() 
