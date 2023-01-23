from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging
import logging

from hacktribe_editor.ht_sysex_utils import init_sysex, build_sysex
from hacktribe_editor.ht_sysex_utils import int_to_midi, calculate_address, syx_addr_len, get_ram_data
from hacktribe_editor.ht_syx_codec import syx_enc
from hacktribe_editor.ht_syx_codec import syx_dec
'''
Hacktribe MIDI System Exclusive messages.

        - Member functions return SysEx messages as bytes.
        - global_channel_channel is global_channel MIDI channel of  device.
        - device is 'hacktribe' | 'sampler' | 'synth'
'''

log = logging.getLogger(__name__)


@log_debug
def search_device(global_channel=0x30, product_id=0x124):
    log.info('search_device not implemented yet')


@log_debug
def get_pattern(index, global_channel=0x30, product_id=0x124):
    '''
    Return Pattern Request SysEx message as bytes

        - Get pattern at index
        - index is int from 0..249
    '''
    sysx = init_sysex('pattern_request', global_channel, product_id)
    sysx.body.index = int_to_midi(index)
    return build_sysex(sysx)


@log_debug
def set_pattern(index, pattern, global_channel=0x30, product_id=0x124):
    '''
    Return Pattern Dump SysEx message as bytes

        - Set pattern at index
        - index is int from 0..249
        - pattern is e2pat as bytes
    '''
    log.info('Called set_pattern')
    sysx = init_sysex('pattern_dump', global_channel, product_id)
    sysx.body.index = int_to_midi(index)
    sysx.body.data = syx_enc(pattern[0x100:])
    return build_sysex(sysx)


@log_debug
def get_current_pattern(global_channel=0x30, product_id=0x124):
    '''
    Return Current Pattern Request SysEx message as bytes

        - Get current pattern edit buffer
    '''
    log.info('Called get_current_pattern')
    sysx = init_sysex('current_pattern_request', global_channel, product_id)
    return build_sysex(sysx)


@log_debug
def set_current_pattern(pattern, global_channel=0x30, product_id=0x124):
    '''
    Return Current Pattern Dump SysEx message as bytes

        - Set current pattern edit buffer
        - pattern is e2pat as bytes
    '''
    log.info('Called get_current_pattern')
    sysx = init_sysex('current_pattern_request', global_channel, product_id)
    return build_sysex(sysx)


@log_debug
def write_pattern(index, global_channel=0x30, product_id=0x124):
    '''
    Return Pattern Write Request SysEx message as bytes

        - Write current edit buffer to pattern at index
        - index is int from 0..249
    '''
    log.info('Called write_pattern')
    sysx = init_sysex('write_pattern', global_channel, product_id)
    sysx.body.index = int_to_midi(index)
    return build_sysex(sysx)


# helper function, uses get_pattern
# get all patterns from device
# returns list of pattern files as sysex bytes
@log_debug
def get_all_patterns(global_channel=0x30, product_id=0x124):
    pass
    #return [get_pattern(i) for i in range(250)]


# helper function, uses set_pattern
# sends all patterns to device
# patterns is list of patterns as sysex bytes
@log_debug
def set_all_patterns(patterns, global_channel=0x30, product_id=0x124):
    log.info('SET ALL PATTERNS: Not implemented yet')


@log_debug
def get_global_channel(global_channel=0x30, product_id=0x124):
    '''
    Return Global Data Request SysEx message as bytes

        - Get global_channel settings
    '''
    log.info('Called get_global_channel')
    sysx = init_sysex('global_channel_request', global_channel, product_id)
    return build_sysex(sysx)


# # val is list of sysex bytes
# def test_sysex_message(val, global_channel=0x30, product_id=0x124):

#     msg = Message('sysex', data=sysex_head + val)
#     outport.send(msg)
#     response = sysex_response()

#     return response


@log_debug
def read_cpu_ram(address, length, global_channel=0x30, product_id=0x124):
    '''
    Return Read CPU RAM Request SysEx message as bytes

        - Read CPU RAM at address for length
        - address is RAM address as int
        - length is read length as int
    '''
    log.info('Called read_cpu_ram')

    # Encode address and length values as sysex
    syx_al = syx_addr_len(address, length)

    sysx = init_sysex('read_cpu_ram', global_channel, product_id)
    sysx.body.addr_len = syx_al
    return build_sysex(sysx)


@log_debug
def write_cpu_ram(address, data, global_channel=0x30, product_id=0x124):
    '''
    Return Write CPU RAM SysEx message as bytes

        - Write data to CPU RAM at address
        - address is RAM address as int
        - data is data to be written as bytes
    '''
    log.info('Called write_cpu_ram')

    sysx_msgs = []

    length = len(data)

    # Encode address and length as sysex
    syx_al = syx_addr_len(address, length)

    # Build first message to set address and length
    sysx = init_sysex('set_write_address', global_channel, product_id)
    sysx.body.addr_len = syx_al
    sysx_msgs += build_sysex(sysx)

    sysx = init_sysex('write_cpu_ram', global_channel, product_id)
    sysx.body.data = syx_enc(data)
    sysx_msgs += build_sysex(sysx)

    return bytes(sysx_msgs)


@log_debug
def read_flash(address, length, global_channel=0x30, product_id=0x124):
    '''
    Return Read Flash Request SysEx message as bytes

        - Read flash at address for length
        - address is flash address as int
        - length is read length as int
    '''
    log.info('Called read_flash')

    # Encode address and length as sysex
    syx_al = syx_addr_len(address, length)

    sysx = init_sysex('read_flash', global_channel, product_id)
    sysx.body.addr_len = syx_al
    return build_sysex(sysx)


@log_debug
def write_flash(address, data, global_channel=0x30, product_id=0x124):
    '''
    Return Write Flash SysEx message as bytes

        - Write data to flash at address
        - address is flash address as int
        - data is data to be written as bytes
    '''
    log.info('write_flash not implemented yet')


@log_debug
def get_ifx(index, global_channel=0x30, product_id=0x124):
    '''
    Return Read CPU RAM Request SysEx messages as bytes

        - Get IFX preset at index
        - index is int from 0..95
    '''
    log.info('Called get_ifx')

    if index > 95 or index < 0:
        log.warning('IFX index out of range - must be >= 0 & < 96.')
        return

    # Calculate IFX preset address
    address = calculate_address(0xc00a80f0, 0x20c, index)
    length = 0x20c

    return read_cpu_ram(address, length)


@log_debug
def set_ifx(index, ifx, global_channel=0x30, product_id=0x124):
    '''
    Return Write CPU RAM SysEx messages as bytes

        - Set IFX preset at index
        - index is int from 0..95
        - ifx is IFX preset as bytes
    '''
    log.info('Called set_ifx')

    sysx_msgs = []

    if index > 95 or index < 0:
        log.warning('IFX index out of range - must be >= 0 & < 96.')
        return

    # Calculate IFX preset address
    address = calculate_address(0xc00a80f0, 0x20c, index)

    # Write IFX preset from CPU RAM
    # Writing in two halves fails less often
    ifx_a = ifx[:0x100]
    sysx_msgs += write_cpu_ram(address, ifx_a)

    ifx_b = ifx[0x100:]
    sysx_msgs += write_cpu_ram(address + 0x100, ifx_b)

    return bytes(sysx_msgs)


@log_debug
def add_ifx(ifx, max_ifx_index, global_channel=0x30, product_id=0x124):
    '''
    Return Write CPU RAM SysEx messages as bytes

        - Add new IFX preset, increasing max_index
        - ifx is IFX preset as bytes
        - max_ifx_index is greatest IFX index as displayed on screen
    '''
    log.info('Called add_ifx')

    sysx_msgs = []

    if max_ifx_index > 95 or max_ifx_index < 0:
        log.warning('IFX index out of range - must be >= 0 & < 96.')
        return

    # Set IFX preset data
    sysx_msgs += set_ifx(max_ifx_index, ifx)

    # Increase limits for menu and saved parameters
    # UPDATE - Add firmware hack to set these values in one location
    sysx_msgs += write_cpu_ram(0xc003efdc, [max_ifx_index + 1])
    sysx_msgs += write_cpu_ram(0xc0048f80, [max_ifx_index])
    sysx_msgs += write_cpu_ram(0xc0049ef0, [max_ifx_index])
    sysx_msgs += write_cpu_ram(0xc004a1f8, [max_ifx_index])
    sysx_msgs += write_cpu_ram(0xc009814c, [max_ifx_index])
    sysx_msgs += write_cpu_ram(0xc0098150, [max_ifx_index + 1])
    sysx_msgs += write_cpu_ram(0xc0098188, [max_ifx_index])
    sysx_msgs += write_cpu_ram(0xc0098194, [max_ifx_index + 1])
    sysx_msgs += write_cpu_ram(0xc00980e8, [max_ifx_index])
    sysx_msgs += write_cpu_ram(0xc00980ec, [max_ifx_index + 1])
    sysx_msgs += write_cpu_ram(0xc009809c, [max_ifx_index + 1])
    sysx_msgs += write_cpu_ram(0xc009811c, [max_ifx_index + 1])
    sysx_msgs += write_cpu_ram(0xc0098138, [max_ifx_index + 1])

    return bytes(sysx_msgs)


@log_debug
def get_max_ifx_index():
    return read_cpu_ram(0xc0048f80, 1)


@log_debug
def set_mfx(index, mfx, global_channel=0x30, product_id=0x124):
    '''
    Return Write CPU RAM SysEx messages as bytes

        - Set MFX preset at index
        - index is int from 0..31
        - mfx is MFX preset as bytes
    '''
    log.info('Called set_mfx')

    sysx_msgs = []

    if index > 31 or index < 0:
        log.warning('MFX index out of range - must be >= 0 & < 32.')
        return

    # Calculate MFX preset address
    address = calculate_address(0xc00b4f30, 0x20c, index)

    # Write MFX preset from CPU RAM
    # Writing in two halves fails less often
    mfx_a = mfx[:0x100]
    sysx_msgs += write_cpu_ram(address, mfx_a)

    mfx_b = mfx[0x100:]
    sysx_msgs += write_cpu_ram(address + 0x100, mfx_b)

    return bytes(sysx_msgs)


@log_debug
def get_mfx(index, global_channel=0x30, product_id=0x124):
    '''
    Return Read CPU RAM Request SysEx messages as bytes

        - Get MFX preset at index
        - index is int from 0..31
    '''
    log.info('Called get_mfx')

    if index > 31 or index < 0:
        log.warning('IFX index out of range - must be >= 0 & < 32.')
        return

    # Calculate MFX preset address
    address = calculate_address(0xc00b4f30, 0x20c, index)
    length = 0x20c

    return read_cpu_ram(address, length)


@log_debug
def get_fx_edit_buffer(index=None, global_channel=0x30, product_id=0x124):
    '''
    Return Read CPU RAM Request SysEx messages as bytes

        - Get FX edit buffer for part
        - index is part 0..16 | 'mfx'
            - 'mfx' == 16
    '''
    log.info('Called get_fx_edit_buffer.')

    if index is not None:
        length = 0x72
        if index == 'mfx':
            index = 0x20

        if index > 0x20 or index < 0:
            log.warning('FX buffer index out of range: must be >= 0 & <= 32.')
            return
    else:
        length = 0x72 * 0x21
        index = 0

    address = 0xc03478a8

    # Calculate address
    address = calculate_address(address, length, index)

    ram = read_cpu_ram(address, length)

    return ram


@log_debug
def set_fx_edit_buffer(fx, global_channel=0x30, product_id=0x124):
    log.warning('set_fx_edit_buffer not implemented yet, use NRPN')


@log_debug
def get_groove(index, global_channel=0x30, product_id=0x124):
    '''
    Return Read CPU RAM Request SysEx messages as bytes

        - Get groove template at index
        - index is int from 0..95
    '''
    log.info('Called get_groove')

    if index > 95 or index < 0:
        log.warning('Groove index out of range - must be >= 0 & < 96.')
        return

    # Calculate groove template address
    address = calculate_address(0xc0143b00, 0x140, index)

    return read_cpu_ram(address, length)


@log_debug
def set_groove(index, groove, global_channel=0x30, product_id=0x124):
    '''
    Return Write CPU RAM SysEx messages as bytes

        - Set groove preset at index
        - index is int from 0..95
        - groove is groove template as bytes
    '''
    log.info('Called set_groove')

    if index > 95 or index < 0:
        log.warning('Groove index out of range - must be >= 0 & < 96.')
        return

    # Calculate IFX preset address
    address = calculate_address(0xc0143b00, 0x140, index)

    return write_cpu_ram(address, groove)


@log_debug
def add_groove(groove,
               max_groove_index,
               global_channel=0x30,
               product_id=0x124):
    '''
    Return Write CPU RAM SysEx messages as bytes

        - Add new groove template, increasing max_index
        - groove is groove template as bytes
        - max_groove_index is one less than greatest groove index displayed on screen
    '''
    log.info('Called add_groove')

    sysx_msgs = []

    if max_groove_index > 95 or max_groove_index < 0:
        log.warning('Groove index out of range - must be >= 0 & < 96.')
        return

    # Set IFX preset data
    sysx_msgs += set_groove(max_groove_index, groove)

    # Increase limits for menu and saved parameters
    # UPDATE - Add firmware hack to set these values in one location
    sysx_msgs += write_cpu_ram(0xc0049da4, [max_groove_index])
    sysx_msgs += write_cpu_ram(0xc007bb90, [max_groove_index])
    sysx_msgs += write_cpu_ram(0xc007bb88, [max_groove_index + 1])
    sysx_msgs += write_cpu_ram(0xc007bb94, [max_groove_index + 1])

    return bytes(sysx_msgs)
