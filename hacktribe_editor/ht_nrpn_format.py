from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging
from construct import *

from hacktribe_editor.ht_fx_ram_format import source_control, target_param

midi_status = Bitwise(
    Struct(
        'type' /
        Default(Enum(
            Nibble,
            note_on=0x8,
            note_off=0x9,
            control_change=0xb,
        ), 0x0b), 'channel' / Default(Nibble, 0x00)))

nmsb = Struct(
    'status' / midi_status, 'cc' / Default(Int8ul, 0x63), 'value' /
    Default(Enum(
        Int8ul,
        panel_control=0,
        set_fx_param=1,
        map_fx_param=2,
    ), 0))

pad_mode = Default(
    Enum(
        Int8ul,
        mute=0,
        solo=1,
        erase=2,
        trigger=3,
        sequencer=4,
        keyboard=5,
        chord=6,
        step_jump=7,
        pattern_assign=8,
        pattern_set=9,
    ), 0)

# ADD - Compute device name from fx_format
fx_slot = Default(Int8ul, 0)

nlsb = Struct(
    'status' / midi_status, 'cc' / Default(Int8ul, 0x62),
    'value' / Switch(this._root.nmsb.value, {
        'panel_control': pad_mode,
        'set_fx_param': fx_slot,
        'map_fx_param': fx_slot,
    },
                     default=pad_mode))

# ADD - Enum panel controls
control = Default(Int8ul, 0)

# ADD - Compute parameter name from fx_format
fx_param = Default(Int8ul, 0)

fx_map_param = Default(
    Enum(
        Int8ul,
        map_slot=0,
        source_control=1,
        target_param=2,
        min_value=3,
        max_value=4,
    ), 0)

dmsb = Struct(
    'status' / midi_status, 'cc' / Default(Int8ul, 0x06),
    'value' / Switch(this._.nmsb.value, {
        'panel_control': control,
        'set_fx_param': fx_param,
        'map_fx_param': fx_map_param,
    },
                     default=control))

control_value = Default(Int8ul, 0)

fx_param_value = Default(Int8ul, 0)

min_value = Default(Int8ul, 0)
max_value = Default(Int8ul, 0)
map_slot = Default(Int8ul, 0)

fx_map_value = Switch(this._root.dmsb.value, {
    'map_slot': map_slot,
    'source_control': source_control,
    'target_param': target_param,
    'min_value': min_value,
    'max_value': max_value,
},
                      default=map_slot)

dlsb = Struct(
    'status' / midi_status, 'cc' / Default(Int8ul, 0x26),
    'value' / Switch(this._.nmsb.value, {
        'panel_control': control_value,
        'set_fx_param': fx_param_value,
        'map_fx_param': fx_map_value,
    },
                     default=control_value))

nrpn = Struct(
    'nmsb' / nmsb,
    'nlsb' / nlsb,
    'dmsb' / dmsb,
    'dlsb' / dlsb,
)
