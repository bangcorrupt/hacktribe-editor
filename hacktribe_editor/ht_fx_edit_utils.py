from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging
from types import SimpleNamespace
import logging
from hacktribe_editor.ht_fmt_utils import init_struct, refresh_struct
from hacktribe_editor.ht_fmt_utils import get_key_index, swap_key_value
from hacktribe_editor.ht_fmt_utils import build_dict, parse_bytes
from hacktribe_editor import ht_fx_ram_format as fxr_fmt
from hacktribe_editor import ht_fx_preset_format as fxp_fmt

log = logging.getLogger(__name__)


@log_debug
def parse_fx_preset(fxp_bytes):
    return parse_bytes(fxp_fmt.preset, fxp_bytes)


@log_debug
def build_fx_preset(fxp_dict):
    return build_dict(fxp_fmt.preset, fxp_dict)


@log_debug
def init_fx_preset(device=None, mfx=False):
    fxp = init_struct(fxp_fmt.preset)
    if device is not None:
        if type(device) == str:
            if mfx:
                fxp.struct.mfx_device = device
                fxp = refresh_fx_preset(fxp)
            else:
                fxp.struct.ifx_1_device = device
                fxp = refresh_fx_preset(fxp)
        elif type(device) == list or type(device) == tuple:
            fxp.struct.ifx_1_device = device[0]
            fxp.struct.ifx_2_device = device[1]
            fxp = refresh_fx_preset(fxp)
    return fxp


@log_debug
def refresh_fx_preset(fxp):
    return refresh_struct(fxp_fmt.preset, fxp)


@log_debug
def get_ifx_dict():
    '''
    Return IFX devices as dict {name: index}
    '''
    ifx_dict = fxp_fmt.ifx_device.subcon.ksymapping
    return swap_key_value(ifx_dict)


@log_debug
def get_mfx_dict():
    '''
    Return MFX devices as dict {name: index}
    '''
    mfx_dict = fxp_fmt.mfx_device.subcon.ksymapping
    return swap_key_value(mfx_dict)


@log_debug
def get_fx_dict():
    '''
    Return FX devices as dict {name: index}
    '''
    return get_ifx_dict() | get_mfx_dict()


@log_debug
def get_fx_type(device):
    if device in get_ifx_dict().keys():
        return 'ifx'
    elif device in get_mfx_dict().keys():
        return 'mfx'


@log_debug
def preset_is_mfx(fxp_dict):
    if fxp_dict['ifx_1_device'] == 'nofx_thru' and fxp_dict[
            'mfx_device'] != 'nofx_mute':
        return True
    else:
        return False


@log_debug
def get_fx_index(device):
    '''
    Return index of FX device
    '''
    fx_idx = get_fx_dict().get(device)
    return fx_idx


@log_debug
def get_fx_device(index):
    '''
    Return FX device name from index
    '''

    mfx_dict = fxp_fmt.mfx_device.subcon.ksymapping
    ifx_dict = fxp_fmt.ifx_device.subcon.ksymapping
    fx_dict = ifx_dict | mfx_dict
    return fx_dict.get(index)


@log_debug
def get_fx_param_index(device, param):
    fxt = get_fx_type(device)
    if fxt == 'ifx':
        dic = {'ifx_1_device': device}
        fxp = refresh_fx_preset(dic)
        return get_key_index(fxp.struct.ifx_1_params, param)
    elif fxt == 'mfx':
        dic = {'mfx_device': device}
        fxp = refresh_fx_preset(dic)
        return get_key_index(fxp.struct.mfx_params, param)



@log_debug
def slice_fx_buffer(buffer):
    return [buffer[i:i + 0x72] for i in range(0, len(buffer), 0x72)]


# FIX - eww
# fxr_list is list of fx buffers as FXEditBuffer
@log_debug
def fx_ram_to_preset(fxeb_list, mfx=False, as_bytes=False):
    log.info("called fx_ram_to_preset")

    # Build default preset
    fxp = fxp_fmt.preset.parse(fxp_fmt.preset.struct.build({}))

    fxr = [eb.container for eb in fxeb_list]

    if mfx:
        fxp.struct.mfx_device = fxr[0].device
        fxp.struct.mfx_pre_level = fxr[0].input_level
        fxp.struct.mfx_post_level = fxr[0].output_level
        refresh_fx_preset(fxp)

        for key in fxr[0].param.keys():
            fxp.struct.mfx_params[key] = fxr[0].param[key]

        i = 0
        for c, control in enumerate(fxr[0].control_map):
            if control.source_control != 0:
                fxp.struct.control_map[
                    i].source_control = control.source_control
                fxp.struct.control_map[i].target_param = control.target_param
                fxp.struct.control_map[i].min_value = control.min_value
                fxp.struct.control_map[i].max_value = control.max_value
                i += 1

    else:
        fxp.struct.ifx_1_device = fxr[0].device
        fxp.struct.ifx_2_device = fxr[1].device
        fxp.struct.ifx_1_pre_level = fxr[0].input_level
        fxp.struct.ifx_2_pre_level = fxr[1].input_level
        fxp.struct.ifx_1_post_level = fxr[0].output_level
        fxp.struct.ifx_2_post_level = fxr[1].output_level

        refresh_fx_preset(fxp)

        for key in fxr[0].param.keys():
            fxp.struct.ifx_1_params[key] = fxr[0].param[key]

        for key in fxr[1].param.keys():
            fxp.struct.ifx_2_params[key] = fxr[1].param[key]

        i = 0
        for c, control in enumerate(fxr[0].control_map):
            if control.source_control != 0:
                fxp.struct.control_map[
                    i].source_control = control.source_control
                fxp.struct.control_map[i].target_param = control.target_param
                fxp.struct.control_map[i].min_value = control.min_value
                fxp.struct.control_map[i].max_value = control.max_value
                i += 1

        for c, control in enumerate(fxr[1].control_map):
            if control.source_control != 0:
                fxp.struct.control_map[
                    i].source_control = control.source_control
                fxp.struct.control_map[i].target_param = control.target_param
                fxp.struct.control_map[i].min_value = control.min_value
                fxp.struct.control_map[i].max_value = control.max_value
                i += 1
    return fxp_fmt.preset.struct.build(fxp.struct)
