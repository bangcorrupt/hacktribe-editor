import logging

from hacktribe_editor.ht_logging import log_debug

from hacktribe_editor.ht_midi import HtMidi
from hacktribe_editor.ht_data import HtData


class HtLib:
    """Top level library object."""

    midi: HtMidi
    """MIDI functions"""

    data: HtData
    """Data functions"""

    @log_debug
    def __init__(self):
        self.midi = HtMidi()
        self.data = HtData()


if __name__ == "__main__":
    ht = HtLib()
