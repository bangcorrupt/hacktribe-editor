import logging
from hacktribe_editor.ht_logging import log_debug


class InputPortError(Exception):
    ''' Raised when a MIDI port can't be opened '''

    @log_debug
    def __init__(self, port):
        self.log = logging.getLogger(__name__)
        self.message = f"Input port '{port}' failed"
        self.log.error(self.message)
        print("\n" + self.message + "\n")
        super().__init__(self.message)


class OutputPortError(Exception):
    ''' Raised when a MIDI port can't be opened '''

    @log_debug
    def __init__(self, port):
        self.log = logging.getLogger(__name__)
        self.message = f"Output port '{port}' failed"
        self.log.error(self.message)
        print("\n" + self.message + "\n")
        super().__init__(self.message)
