from hacktribe_editor.ht_logging import log_debug

from hacktribe_editor.utils import ht_sysex
from hacktribe_editor.utils import ht_nrpn


class HtGrooveMidi:
    """Functions to build  MIDI messages for Hacktribe groove templates."""

    @log_debug
    def __init__(self):
        pass

    @log_debug
    def get_groove(self, index, global_channel=0x30, product_id=0x124):
        """
        Return SysEx message to request groove template.

        :param index:           Index of groove template.
        :param global_channel:  0x30 | Global MIDI channel.
        :param product_id:      Product ID number.

        :return:                SysEx message as bytes.
        """
        return ht_sysex.get_groove(index, global_channel=0x30, product_id=0x124)

    @log_debug
    def set_groove(self, index, groove, global_channel=0x30, product_id=0x124):
        """
        Return SysEx message to set groove template.

        :param index:           Index of groove template.
        :param groove:          Groove template as bytes.
        :param global_channel:  0x30 | Global MIDI channel.
        :param product_id:      Product ID number.

        :return:                SysEx message as bytes.
        """
        return ht_sysex.set_groove(index, groove, global_channel=0x30, product_id=0x124)

    @log_debug
    def add_groove(
        self, groove, max_groove_index, global_channel=0x30, product_id=0x124
    ):
        """
        Return SysEx message to set groove template.

        :param groove:              Groove template as bytes.
        :param max_groove_index:    Index of current maximum groove template.
        :param global_channel:      0x30 | Global MIDI channel.
        :param product_id:          Product ID number.

        :return:                SysEx message as bytes.
        """
        return ht_sysex.add_groove(
            groove, max_groove_index, global_channel=0x30, product_id=0x124
        )
