from hacktribe_editor.ht_logging import log_debug

from hacktribe_editor.utils import ht_sysex
from hacktribe_editor.utils import ht_nrpn


class HtFxMidi:
    """Functions to build  MIDI messages for Hacktribe FX."""

    @log_debug
    def __init__(self):
        pass

    @log_debug
    def get_ifx(self, index, global_channel=0x30, product_id=0x124):
        """
        Returns SysEx message to request IFX preset.

        :param index:           Index of IFX preset.
        :param global_channel:  0x30 | Global MIDI channel.
        :param product_id:      Product ID number.

        :return:                SysEx message as bytes.
        """
        return ht_sysex.get_ifx(index, global_channel, product_id)

    @log_debug
    def set_ifx(self, index, ifx, global_channel=0x30, product_id=0x124):
        """
        Returns SysEx message to set IFX preset.

        :param index:           Index of IFX preset.
        :param ifx              IFX preset data as bytes.
        :param global_channel:  0x30 | Global MIDI channel.
        :param product_id:      Product ID number.

        :return:                SysEx message as bytes.
        """
        return ht_sysex.set_ifx(index, ifx, global_channel, product_id)

    @log_debug
    def add_ifx(self, ifx, max_ifx_index, global_channel=0x30, product_id=0x124):
        return ht_sysex.add_ifx(ifx, max_ifx_index, global_channel, product_id)

    @log_debug
    def get_max_ifx_index(self):
        return ht_sysex.get_max_ifx_index()

    @log_debug
    def set_mfx(self, index, mfx, global_channel=0x30, product_id=0x124):
        return ht_sysex.set_mfx(index, mfx, global_channel, product_id)

    @log_debug
    def get_mfx(self, index, global_channel=0x30, product_id=0x124):
        return ht_sysex.get_mfx(index, global_channel, product_id)

    @log_debug
    def get_edit_buffer(self, index=None, global_channel=0x30, product_id=0x124):
        return ht_sysex.get_fx_edit_buffer(index, global_channel, product_id)

    @log_debug
    def set_param(self, param_index, value, part=0, slot=0):
        return ht_nrpn.set_fx_param(param_index, value, part, slot)

    @log_debug
    def map_param(
        self,
        map_slot,
        source_control,
        target_param,
        min_value,
        max_value,
        part=0,
        slot=0,
    ):
        return ht_nrpn.map_fx_param(
            map_slot,
            source_control,
            target_param,
            min_value,
            max_value,
            part,
            slot,
        )

    @log_debug
    def edit_map(self, map_slot, map_param, param_value, part=0, slot=0):
        return ht_nrpn.edit_fx_map(map_slot, map_param, param_value, part, slot)
