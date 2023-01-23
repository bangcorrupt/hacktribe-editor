import logging
import mido
from time import sleep

from hacktribe_editor.ht_editor import HacktribeEditor
from hacktribe_editor import midi_map as MIDI_MAP

from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging


@log_debug
def main():
    hted = HacktribeEditor()
    control = HtControl(hted)

    input("Press 'Enter' to exit...")


class HtControl:

    @log_debug
    def __init__(self, editor):
        """
        Intialise control.

            - editor is HacktribeEditor
        """

        self.log = logging.getLogger(__name__)
        self.log.info("Initialise HtControl.")

        self.input_channel = 'omni'

        self.hted = editor

        self.midi_map = {
            'control_change': {

                # Set FX device parameter
                MIDI_MAP.FX_PARAM_0_CC:
                lambda value: self.set_fx_param(0, value),
                MIDI_MAP.FX_PARAM_1_CC:
                lambda value: self.set_fx_param(1, value),
                MIDI_MAP.FX_PARAM_2_CC:
                lambda value: self.set_fx_param(2, value),
                MIDI_MAP.FX_PARAM_3_CC:
                lambda value: self.set_fx_param(3, value),
                MIDI_MAP.FX_PARAM_4_CC:
                lambda value: self.set_fx_param(4, value),
                MIDI_MAP.FX_PARAM_5_CC:
                lambda value: self.set_fx_param(5, value),
                MIDI_MAP.FX_PARAM_6_CC:
                lambda value: self.set_fx_param(6, value),
                MIDI_MAP.FX_PARAM_7_CC:
                lambda value: self.set_fx_param(7, value),
                MIDI_MAP.FX_PARAM_8_CC:
                lambda value: self.set_fx_param(8, value),
                MIDI_MAP.FX_PARAM_9_CC:
                lambda value: self.set_fx_param(9, value),
                MIDI_MAP.FX_PARAM_10_CC:
                lambda value: self.set_fx_param(10, value),
                MIDI_MAP.FX_PARAM_11_CC:
                lambda value: self.set_fx_param(11, value),
                MIDI_MAP.FX_PARAM_12_CC:
                lambda value: self.set_fx_param(12, value),
                MIDI_MAP.FX_PARAM_13_CC:
                lambda value: self.set_fx_param(13, value),
                MIDI_MAP.FX_PARAM_14_CC:
                lambda value: self.set_fx_param(14, value),
                MIDI_MAP.FX_PARAM_15_CC:
                lambda value: self.set_fx_param(15, value),
                MIDI_MAP.FX_PARAM_16_CC:
                lambda value: self.set_fx_param(16, value),
                MIDI_MAP.FX_PARAM_17_CC:
                lambda value: self.set_fx_param(17, value),
                MIDI_MAP.FX_PARAM_18_CC:
                lambda value: self.set_fx_param(18, value),
                MIDI_MAP.FX_PARAM_19_CC:
                lambda value: self.set_fx_param(19, value),
                MIDI_MAP.FX_PARAM_20_CC:
                lambda value: self.set_fx_param(20, value),
                MIDI_MAP.FX_PARAM_21_CC:
                lambda value: self.set_fx_param(21, value),
                MIDI_MAP.FX_PARAM_22_CC:
                lambda value: self.set_fx_param(22, value),
                MIDI_MAP.FX_PARAM_23_CC:
                lambda value: self.set_fx_param(23, value),

                # Set FX control map parameter
                # MIDI_MAP.MAP_SRC_CTL_CC:
                # lambda value: self.set_map_param(1, value),
                # MIDI_MAP.MAP_TARG_PARAM_CC:
                # lambda value: self.set_map_param(2, value),
                MIDI_MAP.MAP_MIN_VALUE_CC:
                lambda value: self.set_map_param(3, value),
                MIDI_MAP.MAP_MAX_VALUE_CC:
                lambda value: self.set_map_param(4, value),
            },
            'note_on': {
                # Select channel
                MIDI_MAP.PART_0_NOTE:
                lambda velocity: self.set_channel(0),
                MIDI_MAP.PART_1_NOTE:
                lambda velocity: self.set_channel(1),
                MIDI_MAP.PART_2_NOTE:
                lambda velocity: self.set_channel(2),
                MIDI_MAP.PART_3_NOTE:
                lambda velocity: self.set_channel(3),
                MIDI_MAP.PART_4_NOTE:
                lambda velocity: self.set_channel(4),
                MIDI_MAP.PART_5_NOTE:
                lambda velocity: self.set_channel(5),
                MIDI_MAP.PART_6_NOTE:
                lambda velocity: self.set_channel(6),
                MIDI_MAP.PART_7_NOTE:
                lambda velocity: self.set_channel(7),
                MIDI_MAP.PART_8_NOTE:
                lambda velocity: self.set_channel(8),
                MIDI_MAP.PART_9_NOTE:
                lambda velocity: self.set_channel(9),
                MIDI_MAP.PART_10_NOTE:
                lambda velocity: self.set_channel(10),
                MIDI_MAP.PART_11_NOTE:
                lambda velocity: self.set_channel(11),
                MIDI_MAP.PART_12_NOTE:
                lambda velocity: self.set_channel(12),
                MIDI_MAP.PART_13_NOTE:
                lambda velocity: self.set_channel(13),
                MIDI_MAP.PART_14_NOTE:
                lambda velocity: self.set_channel(14),
                MIDI_MAP.PART_15_NOTE:
                lambda velocity: self.set_channel(15),
                MIDI_MAP.PART_16_NOTE:
                lambda velocity: self.set_channel(16),

                # Select FX map slot
                MIDI_MAP.INC_MAP_SLOT_NOTE:
                lambda velocity: self.increment_map_slot(),
                MIDI_MAP.DEC_MAP_SLOT_NOTE:
                lambda velocity: self.decrement_map_slot(),

                # Set FX control map slot
                # MIDI_MAP.MAP_SLOT_0_NOTE:
                # lambda velocity: self.set_map_slot(0),
                # MIDI_MAP.MAP_SLOT_1_NOTE:
                # lambda velocity: self.set_map_slot(1),
                # MIDI_MAP.MAP_SLOT_2_NOTE:
                # lambda velocity: self.set_map_slot(2),
                # MIDI_MAP.MAP_SLOT_3_NOTE:
                # lambda velocity: self.set_map_slot(3),
                # MIDI_MAP.MAP_SLOT_4_NOTE:
                # lambda velocity: self.set_map_slot(4),
                # MIDI_MAP.MAP_SLOT_5_NOTE:
                # lambda velocity: self.set_map_slot(5),
                # MIDI_MAP.MAP_SLOT_6_NOTE:
                # lambda velocity: self.set_map_slot(6),
                # MIDI_MAP.MAP_SLOT_7_NOTE:
                # lambda velocity: self.set_map_slot(7),
                # MIDI_MAP.MAP_SLOT_8_NOTE:
                # lambda velocity: self.set_map_slot(8),
                # MIDI_MAP.MAP_SLOT_9_NOTE:
                # lambda velocity: self.set_map_slot(9),
            },
        }

        self.hted.midi.register_control_callback(self.midi_callback)

        self.channel = 0
        self.map_slot = 0

    @log_debug
    def set_channel(self, channel, *args):
        """ Set target channel. """

        self.log.info("Called set_channel.")

        self.channel = channel
        print("Selected channel %s, getting edit buffer..." % self.channel)

        if self.channel == 16:
            self.hted.mfxed.refresh_edit_buffer()
        else:
            self.hted.ifxed.refresh_edit_buffer(self.channel)

        print("Received edit buffer for channel %s.\r" % self.channel)

    @log_debug
    def set_fx_param(self, index, value):
        """ Set fx device parameter. """

        self.log.info("Called set_fx_param.")
        if self.channel == 16:
            self.hted.mfxed.set_fx_param(index, value)
        else:
            self.hted.ifxed.set_fx_param(self.channel, index, value)

    @log_debug
    def set_map_slot(self, index, *args):
        """ Set target fx control map slot """

        self.log.info("Called set_map_slot")

        self.map_slot = index
        print("Selected map slot %s." % self.map_slot)

    @log_debug
    def increment_map_slot(self, *args):
        """ Set target fx control map slot """

        self.log.info("Called increment_map_slot")

        self.map_slot = (self.map_slot + 1) % 10
        self.log.info("Selected map slot %s.", self.map_slot)
        print("Selected map slot %s." % self.map_slot)

    @log_debug
    def decrement_map_slot(self, *args):
        """ Set target fx control map slot """

        self.log.info("Called decrement_map_slot")

        self.map_slot = (self.map_slot - 1) % 10
        self.log.info("Selected map slot %s.", self.map_slot)
        print("Selected map slot %s." % self.map_slot)

    @log_debug
    def set_map_param(self, index, value):
        """ Set FX control map parameter. """

        self.log.info("Called set_map_param.")
        if self.channel == 16:
            self.hted.mfxed.set_map_param(self.map_slot, index, value)
        else:
            self.hted.ifxed.set_map_param(self.channel, self.map_slot, index,
                                          value)

    @log_debug
    def midi_callback(self, msg):
        """ Handle MIDI input. """

        self.log.info('Called midi_callback')
        if self.input_channel in ('omni', msg.channel) and msg.type in (
                'control_change', 'note_on'):

            try:
                self.midi_map[msg.type][msg.control if msg.type ==
                                        'control_change' else msg.note](
                                            msg.value if msg.type ==
                                            'control_change' else msg.velocity)
            except:
                self.log.warning("MIDI mapped function failed.")


if __name__ == '__main__':
    main()
