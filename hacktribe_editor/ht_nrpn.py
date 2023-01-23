from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging
import logging

from hacktribe_editor import ht_nrpn_format as nrpn_fmt
'''
Build and parses NRPN messages
    - Functions return NRPN as bytes
'''

log = logging.getLogger(__name__)


@log_debug
def parse(byts):
    ''' Parse NRPN dict to bytes '''
    return nrpn_fmt.nrpn.parse(byts)


@log_debug
def build(dic):
    ''' Build NRPN bytes from dict '''
    return nrpn_fmt.nrpn.build(dic)


@log_debug
def default_dict():
    ''' Initialise default NRPN dict '''
    return parse(build({}))


@log_debug
def get_fx_slot(part, slot):
    ''' Calculate FX slot (0..0x20)
        from part (0..0x10) and slot (0..1 | "mfx") '''

    if part == 'mfx':
        fx_slot = 0x20
    else:
        fx_slot = part * 2 + slot
    return fx_slot


@log_debug
def set_fx_param(param_index, value, part=0, slot=0):

    log.info('Called set_fx_param')
    fx_slot = get_fx_slot(part, slot)

    nrpn_dict = default_dict()
    nrpn_dict.nmsb.value = 'set_fx_param'
    nrpn_dict.nlsb.value = fx_slot
    nrpn_dict.dmsb.value = param_index
    nrpn_dict.dlsb.value = value
    return build(nrpn_dict)


@log_debug
def map_fx_param(map_slot,
                 source_control,
                 target_param,
                 min_value,
                 max_value,
                 part=0,
                 slot=0):

    fx_slot = get_fx_slot(part, slot)

    byts = []
    nrpn_dict = default_dict()
    nrpn_dict.nmsb.value = 'map_fx_param'
    nrpn_dict.nlsb.value = fx_slot

    # Select map slot
    nrpn_dict.dmsb.value = 'map_slot'
    nrpn_dict.dlsb.value = map_slot
    byts += build(nrpn_dict)

    # Set source control
    nrpn_dict.dmsb.value = 'source_control'
    nrpn_dict.dlsb.value = source_control
    byts += build(nrpn_dict)

    # Set target param
    nrpn_dict.dmsb.value = 'target_param'
    nrpn_dict.dlsb.value = target_param
    byts += build(nrpn_dict)

    # Set min value
    nrpn_dict.dmsb.value = 'min_value'
    nrpn_dict.dlsb.value = min_value
    byts += build(nrpn_dict)

    # Select max value
    nrpn_dict.dmsb.value = 'max_value'
    nrpn_dict.dlsb.value = max_value
    byts += build(nrpn_dict)

    return byts


@log_debug
def edit_fx_map(map_slot, map_param, param_value, part=0, slot=0):

    log.info("Called edit_fx_map.")

    byts = []

    fx_slot = get_fx_slot(part, slot)
    nrpn_dict = default_dict()
    nrpn_dict.nmsb.value = 'map_fx_param'
    nrpn_dict.nlsb.value = fx_slot

    # Select map slot
    nrpn_dict.dmsb.value = 'map_slot'
    nrpn_dict.dlsb.value = map_slot
    byts += build(nrpn_dict)

    # Set parameter
    nrpn_dict.dmsb.value = map_param
    nrpn_dict.dlsb.value = param_value
    byts += build(nrpn_dict)

    return byts
