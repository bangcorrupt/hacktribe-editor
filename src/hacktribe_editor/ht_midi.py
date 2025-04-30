from hacktribe_editor.ht_logging import log_debug

from hacktribe_editor.utils import ht_sysex
from hacktribe_editor.utils import ht_nrpn

from hacktribe_editor.ht_fx_midi import HtFxMidi


class HtMidi:
    """Functions to build and parse MIDI messages for Hacktribe."""

    fx: HtFxMidi
    """FX MIDI functions."""

    @log_debug
    def __init__(self):
        self.fx = HtFxMidi()

    @log_debug
    def parse_nrpn(self, nrpn_bytes):
        """
        Receives one full NRPN message as bytes and converts it to a dictionary.

        :param nrpn_bytes: One full NRPN message as bytes.

        :return: NRPN message as dict.
        """

        return ht_nrpn.parse(nrpn_bytes)

    @log_debug
    def parse_sysex(self, sysex_bytes):
        """
        Receives one full SysEx message as bytes and converts it to a dictionary.

        :param sysex_bytes: One full SysEx message as bytes.

        :return: SysEx message as dict.
        """

        return ht_sysex.parse(sysex_bytes)
