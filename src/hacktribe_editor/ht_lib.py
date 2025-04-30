import logging

from hacktribe_editor_api.ht_logging import log_debug

from hacktribe_editor_api import ht_sysex
from hacktribe_editor_api import ht_nrpn


class HtFxMidi:
    @log_debug
    def __init__(self):
        pass

    @log_debug
    def get_ifx(index, global_channel=0x30, product_id=0x124):
        return ht_sysex.get_ifx(index, global_channel, product_id)

    @log_debug
    def set_ifx(index, ifx, global_channel=0x30, product_id=0x124):
        return ht_sysex.set_ifx(index, ifx, global_channel, product_id)

    @log_debug
    def add_ifx(ifx, max_ifx_index, global_channel=0x30, product_id=0x124):
        return ht_sysex.add_ifx(ifx, max_ifx_index, global_channel, product_id)

    @log_debug
    def get_max_ifx_index():
        return ht_sysex.get_max_ifx_index()

    @log_debug
    def set_mfx(index, mfx, global_channel=0x30, product_id=0x124):
        return ht_sysex.set_mfx(index, mfx, global_channel, product_id)

    @log_debug
    def get_mfx(index, global_channel=0x30, product_id=0x124):
        return ht_sysex.get_mfx(index, global_channel, product_id)

    @log_debug
    def get_edit_buffer(index=None, global_channel=0x30, product_id=0x124):
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


class HtMidi:
    @log_debug
    def __init__(self):
        self.fx = HtFxMidi()

    @log_debug
    def parse_nrpn(self, nrpn_bytes):
        """Receives one full NRPN message as bytes, returns dict."""

        return ht_nrpn.parse(nrpn_bytes)

    @log_debug
    def parse_sysex(self, sysex_bytes):
        """Receives one full sysex message as bytes, returns dict."""

        return ht_sysex.parse(sysex_bytes)


class HtData:
    @log_debug
    def __init__(self):
        pass


class HtLib:
    @log_debug
    def __init__(self):
        self.midi = HtMidi()
        self.data = HtData()
