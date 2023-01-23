import sys
from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging
import logging

from hacktribe_editor.ht_midi import HtMIDI


class HtEdit:

    @log_debug
    def __init__(self, midi):

        self.log = logging.getLogger(__name__)
        self.log.info('Initialise %s.', self.__class__.__name__)

        self.midi = midi

