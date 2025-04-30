import logging

from hacktribe_editor.ht_logging import log_debug

from hacktribe_editor.ht_fx_midi import HtFxMidi

from hacktribe_editor.utils import ht_sysex
from hacktribe_editor.utils import ht_nrpn


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
