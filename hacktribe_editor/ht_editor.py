import sys
import logging
from pathlib import Path

from hacktribe_editor.ht import Ht
from hacktribe_editor import ht_editor_config as hte_cfg
from hacktribe_editor.ht_midi import HtMIDI
from hacktribe_editor.ht_ifx_editor import HtIFXEditor
from hacktribe_editor.ht_mfx_editor import HtMFXEditor
from hacktribe_editor.ht_logging import log_debug
import hacktribe_editor.ht_logging


@log_debug
def main():
    hted = HacktribeEditor()


class HacktribeEditor:

    @log_debug
    def __init__(self, config_path=None):
        self.log = logging.getLogger(__name__)

        self.log.info('Initialise HacktribeEditor.')

        self.config_path = config_path
        self.auto_write_config = True

        self._ht = None
        self._config = None
        self._midi = None
        self._ifxed = None
        self._mfxed = None

    @property
    @log_debug
    def ht(self):
        if self._ht is None:
            self.init_ht()
        return self._ht

    @ht.setter
    @log_debug
    def ht(self, ht):
        self._ht = ht

    @property
    @log_debug
    def config(self):
        if self._config is None:
            self.init_config()
        return self._config

    @config.setter
    @log_debug
    def config(self, config):
        self._config = config

    @property
    @log_debug
    def midi(self):
        if self._midi is None:
            self.init_midi()
        return self._midi

    @midi.setter
    @log_debug
    def midi(self, midi):
        self._midi = midi

    @property
    @log_debug
    def ifxed(self):
        if self._ifxed is None:
            self.init_ifxed()
        return self._ifxed

    @ifxed.setter
    @log_debug
    def ifxed(self, ifxed):
        self._ifxed = ifxed

    @property
    @log_debug
    def mfxed(self):
        if self._mfxed is None:
            self.init_mfxed()
        return self._mfxed

    @mfxed.setter
    @log_debug
    def mfxed(self, mfxed):
        self._mfxed = mfxed

    @log_debug
    def init_ht(self):
        self.log.info("Called init_ht.")
        try:
            self.ht = Ht()  # Load last session / config?
            self.log.info("Ht initialisation succeeded.")
        except:
            self.log.warning("Ht initialisation failed.")
            sys.exit(0)

    @log_debug
    def init_config(self):
        self.log.info('Called init_config.')
        try:
            if self.config_path is not None:
                self.config = hte_cfg.open_config(self.config_path)
            else:
                self.config = hte_cfg.open_config()

            self.log.info('Configuration initialisation succeeded.')
        except:
            self.log.warning(
                'Configuration initialisation failed, check config_path.')
            sys.exit(0)

    @log_debug
    def init_midi(self):
        self.log.info('Called init_midi.')

        inport = self.config['midi']['input']
        outport = self.config['midi']['output']
        control_port = self.config['midi']['control']['input']
        try:
            self.midi = HtMIDI(inport, outport, control_port)
            self.log.info('MIDI initialisation succeeded.')
        except:
            self.log.warning(
                'MIDI initialisation failed, check device and configuration.')
            sys.exit(0)

    @log_debug
    def init_ifxed(self):
        self.log.info('Called init_ifxed.')
        try:
            self.ifxed = HtIFXEditor(self.midi)
            self.log.info('FX editor initialisation succeeded.')
        except:
            self.log.warning('FX editor initialisation failed.')
            sys.exit(0)

    @log_debug
    def init_mfxed(self):
        self.log.info('Called init_mfxed.')
        try:
            self.mfxed = HtMFXEditor(self.midi)
            self.log.info('FX editor initialisation succeeded.')
        except:
            self.log.warning('FX editor initialisation failed.')
            sys.exit(0)

    @log_debug
    def reload_config(self):
        self.init_config()
        self.init_midi()

    @log_debug
    def write_config(self):
        hte_cfg.write_config(self.config)

    @log_debug
    def save_file(self, path, data):
        with open(path, 'wb') as f:
            f.write(data)


if __name__ == '__main__':
    main()
