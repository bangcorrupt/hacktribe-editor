import logging

from hacktribe_editor import ht_nrpn as nrpn
from hacktribe_editor import ht_sysex as sysx
from hacktribe_editor import ht_fx_ram_format as fxr_fmt
from hacktribe_editor import ht_fx_preset_format as fxp_fmt
from hacktribe_editor import ht_fx_edit_utils as fxed_utils
from hacktribe_editor import ht_sysex_utils as sysx_utils
from hacktribe_editor.ht_edit import HtEdit
from hacktribe_editor.ht_fx_editor import HtFXEditor
from hacktribe_editor.ht_format import HtMFXEditBuffer, HtFXPreset
from hacktribe_editor.ht_logging import log_debug


@log_debug
def main():
    mfxed = HtMFXEditor()


class HtMFXEditor(HtEdit):
    """
    Manipulate MFX Edit Buffer.

        - buffer is mfx edit buffer as HtMFXEditBuffer
        - midi is HtMIDI
    """

    FXBuffer = HtMFXEditBuffer

    @log_debug
    def __init__(self, midi=None, buffer=None):
        super().__init__(midi)

        # FX edit buffer as HtMFXEditBuffer
        self._buffer = buffer

    @property
    @log_debug
    def buffer(self):
        """ Get buffer """

        self.log.info("Called buffer.")
        if self._buffer is None:
            self.refresh_edit_buffer()
        return self._buffer

    @buffer.setter
    @log_debug
    def buffer(self, buffer):
        """ Set buffer """

        self._buffer = buffer

    @property
    @log_debug
    def max_fx_param(self):
        """ Get maximum available fx parameter index. """

        self.log.info("Called max_fx_param.")
        max_fx_param = len(list(self.buffer.param))
        self.log.info("Maximum MFX param: %s.", max_fx_param)
        return max_fx_param

    @property
    @log_debug
    def fx_device_name(self):
        """ Get name of fx device as string. """

        return self.buffer.device

    @property
    @log_debug
    def fx_param_names(self):
        """ Get names of fx device parameters as list of strings. """

        return list(self.buffer.param.keys())

    @property
    @log_debug
    def map_param_names(self):
        """ Get fx map param names as list of strings. """

        self.log.info("Called map_param_names.")
        return list(self.buffer.control_map[0])

    @log_debug
    def refresh_edit_buffer(self):
        """
        Get a fresh copy of fx edit buffer from device
        """

        self.log.info("Called refresh_edit_buffer.")

        fxeb = sysx_utils.get_ram_data(
            self.midi.send_sysex(sysx.get_fx_edit_buffer(0x20)))

        self._buffer = self.FXBuffer(fxeb)

    @log_debug
    def set_fx_param(self, param_index, value):
        '''
        Set FX parameter via NRPN.
        '''

        self.log.info('Called set_fx_param.')

        if param_index < self.max_fx_param:
            self.log.info('set_fx_param:  device=%s, param=%s, value=%s.',
                          self.buffer.device,
                          list(self.buffer.param)[param_index], value)

            print('set_fx_param:  device=%s, param=%s, value=%s.',
                  self.buffer.device,
                  list(self.buffer.param)[param_index], value)

            nrpn_msg = nrpn.set_fx_param(param_index, value, 0x10, 0)
            self.midi.send_bytes(nrpn_msg)
            self.update_fx_buffer(param_index, value)

        else:
            self.log.warning("Parameter index %s out of range.", param_index)

    @log_debug
    def update_fx_buffer(self, param_index, value):
        '''
        Update parameter value in local edit buffer.
        '''

        self.log.info('Called update_local_buffer: param=%s, value=%s.',
                      self.fx_param_names[param_index], value)

        self.buffer.param[self.fx_param_names[param_index]] = value

    @log_debug
    def update_map_buffer(self, map_slot, param_index, value):
        """ Update local buffer. """

        self.log.info("Called update_map_buffer.")

        self.buffer.control_map[map_slot][self.map_param_names[param_index -
                                                               1]] = value

    @log_debug
    def get_current_preset(self, channel=0x10):
        """
        Return current MFX as HtMFXPreset
        """

        self.log.info("Called get_current_preset.")

        fxpb = fxed_utils.fx_ram_to_preset([self.buffer],
                                           mfx=True,
                                           as_bytes=True)

        return HtFXPreset(fxpb)

    @log_debug
    def get_preset(self, index):
        """ Return preset at index from device. """

        self.log.info("Called get_preset.")

        fxp_bytes = sysx_utils.get_ram_data(
            self.midi.send_sysex(sysx.get_mfx(index)))

        return HtFXPreset(fxp_bytes)

    @log_debug
    def set_preset(self, index, preset):
        """
        Set preset at index on device.

            - preset is HtFXPreset
        """

        self.log.info("Called set_fx_preset.")

        self.midi.send_sysex(sysx.set_mfx(index, preset.bytes))

    @log_debug
    def set_map_param(self, map_slot, param_index, value):
        """
        Set FX control map parameter via NRPN.
        """

        self.log.info("Called set_map_param.")

        self.log.info(
            "set_map_param: part: MFX, map_slot=%s, map_param=%s, value=%s.",
            map_slot, param_index, value)

        nrpn_msg = nrpn.edit_fx_map(map_slot,
                                    param_index,
                                    value,
                                    part=16,
                                    slot=0)
        self.midi.send_bytes(nrpn_msg)

        self.update_map_buffer(map_slot, param_index, value)


if __name__ == '__main__':
    main()
