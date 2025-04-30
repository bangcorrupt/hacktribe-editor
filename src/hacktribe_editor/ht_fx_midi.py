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
        """
        Returns SysEx message to add new IFX preset.

        :param ifx              IFX preset data as bytes.
        :param max_ifx_index:   Index of current maximum IFX preset.
        :param global_channel:  0x30 | Global MIDI channel.
        :param product_id:      Product ID number.

        :return:                SysEx message as bytes.
        """
        return ht_sysex.add_ifx(ifx, max_ifx_index, global_channel, product_id)

    @log_debug
    def get_max_ifx_index(self):
        """
        Returns SysEx message to request index of current maximum IFX preset.

        :return:                SysEx message as bytes.
        """
        return ht_sysex.get_max_ifx_index()

    @log_debug
    def get_mfx(self, index, global_channel=0x30, product_id=0x124):
        """
        Returns SysEx message to request MFX preset.

        :param index:           Index of MFX preset.
        :param global_channel:  0x30 | Global MIDI channel.
        :param product_id:      Product ID number.

        :return:                SysEx message as bytes.
        """
        return ht_sysex.get_mfx(index, global_channel, product_id)

    @log_debug
    def set_mfx(self, index, mfx, global_channel=0x30, product_id=0x124):
        """
        Returns SysEx message to set MFX preset.

        :param index:           Index of MFX preset.
        :param mfx              MFX preset data as bytes.
        :param global_channel:  0x30 | Global MIDI channel.
        :param product_id:      Product ID number.

        :return:                SysEx message as bytes.
        """
        return ht_sysex.set_mfx(index, mfx, global_channel, product_id)

    @log_debug
    def get_edit_buffer(self, index=None, global_channel=0x30, product_id=0x124):
        """
        Returns SysEx message to request FX edit buffer.

        :param index:           Index of preset, or 'mfx', or None for all.
        :param global_channel:  0x30 | Global MIDI channel.
        :param product_id:      Product ID number.

        :return:                SysEx message as bytes.
        """
        return ht_sysex.get_fx_edit_buffer(index, global_channel, product_id)

    @log_debug
    def set_param(self, param_index, value, part=0, slot=0):
        """
        Returns NRPN message to set FX parameter.

        :param param_index:     Index of parameter in FX device.
        :param value:           Value to set.
        :param part:            Part 0..16 or 'mfx'.
        :param slot:            FX device slot 0..1.

        :return:                NRPN message as bytes.
        """
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
        """
        Returns NRPN message to map control to FX parameter.

        :param map_slot:        Index of control map slot.
        :param source_control:  Index of source control.
        :param target_param:    Index of target parameter in FX device.
        :param min_value:       Minimum value of control mapping.
        :param max_value:       Maximum value of control mapping.
        :param part:            Part 0..16 or 'mfx'.
        :param slot:            FX device slot 0..1.

        :return:                NRPN message as bytes.
        """
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
        """
        Returns NRPN message to edit single parameter of FX control map.

        :param map_slot:        Index of control map slot.
        :param map_param:       Index of parameter in control map.
        :param value:           Value to set.
        :param part:            Part 0..16 or 'mfx'.
        :param slot:            FX device slot 0..1.

        :return:                NRPN message as bytes.
        """
        return ht_nrpn.edit_fx_map(map_slot, map_param, param_value, part, slot)
