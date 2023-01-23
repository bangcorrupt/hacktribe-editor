from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging
from hacktribe_editor.ht_fmt_utils import build_dict, parse_bytes
from hacktribe_editor.ht_fmt_utils import init_struct
from hacktribe_editor import ht_sysex_format as sysx_fmt
from hacktribe_editor.ht_syx_codec import syx_enc
from hacktribe_editor.ht_syx_codec import syx_dec
'''
Utility functions for ht_sysex and ht_sysex_format
'''


@log_debug
def init_sysex(msg_id='current_pattern_request',
               global_channel=0x30,
               product_id=0x124):
    '''
    Return Hacktribe SysEx message as dict
        - msg_id is ht_sysex_format.msg_id as string
        - global_channel is global MIDI channel + 0x30
        - product_id is 0x123 | 0x124
    '''
    sysx = init_struct(sysx_fmt.sysex)
    sysx.msg_id = msg_id
    return sysx


# convert integer x <= 255 to 2 midi bytes
# returns little endian tuple
@log_debug
def int_to_midi(self, x):
    return (x % 128, x // 128)


@log_debug
def build_sysex(sysx_dict):
    return build_dict(sysx_fmt.sysex, sysx_dict)


@log_debug
def parse_sysex(sysx_bytes):
    return parse_bytes(sysx_fmt.sysex, sysx_bytes)


@log_debug
def calculate_address(base, length, index):
    return base + length * index


@log_debug
def syx_addr_len(address, length):
    addr = address.to_bytes(4, byteorder='little')
    leng = length.to_bytes(4, byteorder='little')
    return syx_enc(addr + leng)


@log_debug
def get_ram_data(sysx_bytes):

    sysx = parse_sysex(sysx_bytes)
    data = syx_dec(sysx.body.data[2:])
    return data


@log_debug
def mod_channel_id(msg, global_channel, product_id):
    global_channel += 0x30
    sysx_dict = parse_sysex(msg)
    sysx_dict.global_channel = global_channel
    sysx_dict.product_id = product_id
    return build_sysex(sysx_dict)
