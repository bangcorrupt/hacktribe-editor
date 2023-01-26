from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging
import sys
from functools import wraps
import mido
import logging
from time import sleep

from hacktribe_editor import ht_logging
from hacktribe_editor import ht_sysex_utils as sysx_utils


@log_debug
def main():

    inport = 'electribe2 sampler:electribe2 sampler electribe2 s'
    outport = 'electribe2 sampler:electribe2 sampler electribe2 s'
    callback = print_midi
    controls = ['MIDI Mix:MIDI Mix MIDI 1', 'MPK mini 3:MPK mini 3 MIDI 1']
    midi = HtMIDI(inport, outport, control_port=controls, callback=callback)
    while (True):
        sleep(1)


@log_debug
def print_midi(msg):
    print(msg)


class HtMIDI:
    sysex_send_sleep = 0.3

    @log_debug
    def __init__(self,
                 inport,
                 outport,
                 control_port=None,
                 global_channel=0,
                 device='hacktribe',
                 callback=None):
        '''
        MIDI class for Hacktribe.

        Configures MIDI communication.
            - inport is input port name as string
            - outport is output port name as string
            - control_port is control port name as string or list of strings
            - global_channel is int (0..15)
            - device is ('hacktribe' | 'sampler' | 'synth') | (0x124 | 0x123)
            - callback is function or list of functions
                - called when MIDI msg received
        '''

        self.log = logging.getLogger(__name__)
        self.log.info('Initialise HtMIDI')

        self.global_channel = global_channel + 0x30

        self.sysex_response = None

        # Reduces log spam
        self.ignore_clock = True

        if isinstance(device, int):
            self.product_id = device
        else:
            self.product_id = 0x123 if device == 'synth' else 0x124

        try:
            self.inport = mido.open_input(inport) if isinstance(
                inport, str) else inport
            self.log.info('Input port: %s', self.inport.name)
        except:
            self.log.error("Error: inport is required")
            sys.exit(0)

        try:
            self.outport = mido.open_output(outport) if isinstance(
                outport, str) else outport
            self.log.info('Output port: %s', self.outport.name)
        except:
            self.log.error("Error: outport is required")
            sys.exit(0)

        self.inport.callback = self.input_callback

        self.input_callbacks = []
        if callback is not None:
            self.register_callback(callback)

        self.control_ports = [
            mido.open_input(name='HACKTRIBE_EDITOR_CONTROL', virtual=True)
        ]
        if control_port is not None:
            self.add_control_port(control_port)

        self.control_callbacks = []
        for port in self.control_ports:
            try:
                port.callback = self.control_callback
            except:
                self.log.error(
                    "Error: Failed to add control_callback: port=%s.",
                    port.name)

    @log_debug
    def register_callback(self, callback):
        callback = [callback] if not isinstance(callback, list) else callback
        for function in callback:
            self.input_callbacks.append(function)

    @log_debug
    def register_control_callback(self, callback):
        self.log.info("Called register_control_callback.")

        callback = [callback] if not isinstance(callback, list) else callback
        for function in callback:
            self.control_callbacks.append(function)

    @log_debug
    def add_control_port(self, control_port):
        self.log.info("Called add_control_port.")

        control_port = [
            control_port
        ] if not isinstance(control_port, list) else control_port

        try:
            control_port = [
                mido.open_input(port) if isinstance(port, str) else port
                for port in control_port
            ]
            self.log.info("Added control port.")
        except:
            self.log.error("Error: mido could not open control_port")
            sys.exit(0)

        for port in control_port:
            if port ins not None:
                self.control_ports.append(port)
                self.log.info("Added control_port: %s", port.name)

    # clock log spam
    # @log_debug
    def input_callback(self, msg):
        # Ignore clock
        if msg.type == 'clock' and self.ignore_clock:
            return

        self.log.info('Called input_callback')
        self.log.info('Received MIDI: ' +
                      (str(msg)[:64] +
                       '...') if len(str(msg)) > 64 else str(msg))

        if msg.type == 'sysex':
            self.sysex_callback(msg)

        self.external_callbacks(msg)

    @log_debug
    def control_callback(self, msg):
        self.log.info("Called control_callback")
        for callback in self.control_callbacks:
            callback(msg)

    @log_debug
    def sysex_callback(self, msg):
        self.log.info('Called sysex_callback')
        self.sysex_response = bytes(msg.bytes())

    @log_debug
    def external_callbacks(self, msg):
        self.log.info("Called external_callbacks.")
        for callback in self.input_callbacks:
            callback(msg)

    @log_debug
    def send_bytes(self, msg_bytes, receive=False):
        self.log.info('Called send_bytes.')
        # Convert bytes to mido.Message
        messages = mido.parse_all(list(msg_bytes))
        # Send MIDI
        for msg in messages:
            self.log.info('Sending MIDI: ' +
                          (str(msg)[:64] +
                           '...') if len(str(msg)) > 64 else str(msg))

            self.outport.send(msg)
            if msg.type == 'sysex':
                sleep(HtMIDI.sysex_send_sleep)

    @log_debug
    def send_sysex(self, msg, receive=True, timeout=False):
        self.log.info('Called send_sysex.')

        if type(msg) == mido.Message:
            msg = bytes(msg.bytes)

        # FIX - Update global channel if not 0
        # msg = sysx_utils.mod_channel_id(msg, self.global_channel,
        #                                 self.product_id)
        self.send_bytes(msg)

        if receive:
            self.log.info('Waiting for SysEx response...')
            response = self.receive_sysex(timeout)
            return response

    @log_debug
    def receive_sysex(self, timeout=False):
        self.log.info('Called receive_sysex.')
        while self.sysex_response is None:
            sleep(0.1)
        self.log.info('Received SysEx response.')
        response = self.sysex_response
        self.sysex_response = None
        return response


if __name__ == '__main__':
    main()
