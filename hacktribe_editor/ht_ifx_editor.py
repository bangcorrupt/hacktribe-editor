from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging
import logging

from hacktribe_editor import ht_nrpn as nrpn
from hacktribe_editor import ht_sysex as sysx
from hacktribe_editor import ht_fx_ram_format as fxr_fmt
from hacktribe_editor import ht_fx_preset_format as fxp_fmt
from hacktribe_editor import ht_fx_edit_utils as fxed_utils
from hacktribe_editor import ht_sysex_utils as sysx_utils

from hacktribe_editor.ht_edit import HtEdit
from hacktribe_editor.ht_format import HtIFXEditBuffer, HtFXPreset


@log_debug
def main():
    fxed = HtFXEditor()


class HtIFXEditor(HtEdit):
    """
    Manipulate FX Edit Buffer.

        - buffer is fx edit buffer as list of HtFXEditBuffer
        - midi is HtMIDI
    """

    FXBuffer = HtIFXEditBuffer
    fx_buffer_count = 0

    @log_debug
    def __init__(self, midi=None, buffer=None):
        super().__init__(midi)

        # FX edit buffer as list of HtIFXEditBuffer
        self._buffer = buffer

    @property
    @log_debug
    def buffer(self):
        """ Get buffer. """

        self.log.info("Called buffer.")
        if self._buffer is None:
            self.refresh_edit_buffer(channel=0)
        return self._buffer

    @buffer.setter
    @log_debug
    def buffer(self, buffer):
        """ Set buffer """

        self.log.info("Set buffer")
        self._buffer = buffer

    @property
    @log_debug
    def max_fx_param(self):
        """ Get maximum available fx parameters for each slot as list """

        self.log.info("Called max_fx_param.")

        max_fx_param = [
            len(list(self.buffer[index].param)) for index in range(2)
        ]

        self.log.info("Maximum IFX param: %s.", sum(max_fx_param) - 1)

        return max_fx_param

    @property
    @log_debug
    def fx_device_name(self):
        """ Get name of fx device as string. """

        return [buffer.device for buffer in self.buffer]

    @property
    @log_debug
    def fx_param_names(self):
        """ Get names of fx device parameters as list of strings. """

        return [list(buffer.param.keys()) for buffer in self.buffer]

    @property
    @log_debug
    def max_preset_index(self):
        """ Get greatest index of preset on device. """
        return sysx_utils.parse_sysex(
            self.midi.send_sysex(sysx.get_max_ifx_index())).body.data[-1] + 1

    @property
    @log_debug
    def configured_map_slots(self):
        """ Get list of configured map slots """
        self.log.info("Called configured_map_slots.")

        # Indices of configured map slots in each buffer
        configured_slots = [[
            index for index in range(10)
            if buffer.control_map[index]['source_control'] != 0
        ] for buffer in self.buffer]

        return configured_slots[0] + configured_slots[1]

    @property
    @log_debug
    def map_param_names(self):
        """ Get fx map param names as list of strings. """

        self.log.info("Called map_param_names.")
        return list(self.buffer[0].control_map[0])

    @log_debug
    def refresh_edit_buffer(self, channel):
        """
        Return full edit buffer as list of HtFXEditBuffer.
        """

        self.log.info("Called get_edit_buffer.")

        slots = [channel * 2, channel * 2 + 1]

        fxeb = [
            sysx_utils.get_ram_data(
                self.midi.send_sysex(sysx.get_fx_edit_buffer(index)))
            for index in slots
        ]

        self.buffer = [self.FXBuffer(data) for data in fxeb]

    @log_debug
    def set_fx_param(self, channel, param_index, value):
        '''
        Set FX parameter via NRPN.
        '''

        self.log.info('Called set_fx_param.')

        if param_index >= self.max_fx_param[0]:
            param_index -= self.max_fx_param[0]
            fx_slot = 1
            self.log.info("FX slot 1")
        else:
            fx_slot = 0
            self.log.info("FX slot 0")

        if param_index < self.max_fx_param[fx_slot]:
            self.log.info(
                'set_fx_param: part=%s, slot=%s, device=%s, param=%s, value=%s.',
                channel, fx_slot, self.fx_device_name[fx_slot],
                self.fx_param_names[fx_slot][param_index], value)

            print(
                'set_fx_param: part=%s, slot=%s, device=%s, param=%s, value=%s.'
                % (channel, fx_slot, self.fx_device_name[fx_slot],
                   self.fx_param_names[fx_slot][param_index], value))

            nrpn_msg = nrpn.set_fx_param(param_index, value, channel, fx_slot)

            self.midi.send_bytes(nrpn_msg)
            self.update_fx_buffer(fx_slot, param_index, value)

        else:
            self.log.warning(
                "Parameter index out of range, maximum parameter index is %s.",
                sum(self.max_fx_param) - 1)

            print(
                "Parameter index out of range, maximum parameter index is %d."
                % (sum(self.max_fx_param) - 1))

    @log_debug
    def set_map_param(self, channel, map_slot, param_index, value):
        """
        Set FX control map parameter via NRPN.
        """

        self.log.info("Called set_map_param.")

        if map_slot in self.configured_map_slots:

            self.log.info(
                "set_map_param: part:%s, map_slot=%s, map_param=%s, value=%s.",
                channel, map_slot, param_index, value)

            fx_slot = self.get_map_fx_slot(map_slot)

            if fx_slot is not None:
                nrpn_msg = nrpn.edit_fx_map(map_slot,
                                            param_index,
                                            value,
                                            part=channel,
                                            slot=fx_slot)
                self.midi.send_bytes(nrpn_msg)

                self.update_map_buffer(map_slot, fx_slot, param_index, value)

                print(
                    "set_map_param: part:%s, map_slot=%s, map_param=%s, value=%s."
                    % (channel, map_slot,
                       self.map_param_names[param_index - 1], value))

            else:
                self.log.info("Map slot %s misconfigured.", map_slot)
                print("Map slot %s misconfigured." % (map_slot))
        else:
            self.log.info("Map slot %s not configured.", map_slot)
            print("Map slot %s not configured." % (map_slot))

    @log_debug
    def get_map_fx_slot(self, map_index):
        """ Return first matching fx slot where map slot at index is configured, else None. """

        self.log.info("Called get_map_fx_slot.")

        if self.buffer[0].control_map[map_index]['source_control'] != 0:
            return 0
        elif self.buffer[1].control_map[map_index]['source_control'] != 0:
            return 1
        else:
            return None

    @log_debug
    def update_fx_buffer(self, fx_slot, param_index, value):
        '''
        Update parameter value in local edit buffer.
        '''

        self.log.info('Called update_local_buffer: param=%s, value=%s.',
                      self.fx_param_names[fx_slot][param_index], value)

        self.buffer[fx_slot].param[self.fx_param_names[fx_slot]
                                   [param_index]] = value

    @log_debug
    def update_map_buffer(self, map_slot, fx_slot, param_index, value):
        """ Update local buffer. """

        self.log.info("Called update_map_buffer.")

        self.buffer[fx_slot].control_map[map_slot][self.map_param_names[
            param_index - 1]] = value

    @log_debug
    def get_preset(self, index):
        """ Return preset at index from device. """

        fxp_bytes = sysx_utils.get_ram_data(
            self.midi.send_sysex(sysx.get_ifx(index)))

        return HtFXPreset(fxp_bytes)

    @log_debug
    def set_preset(self, index, preset):
        """
        Set preset at index on device.

            - preset is HtFXPreset
        """

        self.log.info("Called set_fx_preset.")

        self.midi.send_sysex(sysx.set_ifx(index, preset.bytes))

    @log_debug
    def get_current_preset(self, channel):
        """
        Return current FX of channel as HtFXPreset
        """

        self.log.info("Called get_current_preset.")

        # Current hack does not update device edit buffer,
        # only sends values to DSP.
        #
        # self.refresh_edit_buffer(channel)

        fxp = fxed_utils.fx_ram_to_preset(self.buffer, as_bytes=True)

        return HtFXPreset(fxp)

    @log_debug
    def add_preset(self, preset):
        """
        Add preset to device.

            - preset is FX preset as HtFXPreset
        """

        self.log.info("Called add preset.")
        self.midi.send_sysex(sysx.add_ifx(preset.bytes, self.max_preset_index))


if __name__ == '__main__':
    main()
