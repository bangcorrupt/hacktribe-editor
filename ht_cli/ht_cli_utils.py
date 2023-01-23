import logging
import click
from mido import get_input_names, get_output_names, open_input, open_output

from hacktribe_editor.ht_editor import HacktribeEditor
from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging

log = logging.getLogger(__name__)

pass_hted = click.make_pass_decorator(HacktribeEditor, ensure=True)


@log_debug
def get_ports(filt=None, output=False):
    if output:
        ports = get_output_names()
    else:
        ports = get_input_names()

    if filt is not None:
        return [p for p in ports if filt in p]
    else:
        return ports


@log_debug
def prompt_ports(filt=None, output=False):
    if output:
        prefix = "\nAvailable output ports:\n"
        ports = get_output_names()
        suffix = "\nOutput port"
    else:
        prefix = "\nAvailable input ports:\n"
        ports = get_input_names()
        suffix = "\nInput port"

    if filt is not None:
        prompt = [n + "\n" for n in ports if filt in n]
        if prompt == []:
            prompt = ["No input ports found (filter='" + filt + "')\n"]
        prompt = "\n" + prefix + ''.join(prompt) + suffix
        return prompt
    else:
        prompt = "\n" + prefix + ''.join([n + "\n" for n in ports]) + suffix
        return prompt


@log_debug
def test_port(port, output=False):

    if output:
        try:
            open_input(port)
            log.info("MIDI input port '%s' is working", port)
            return True
        except:
            log.warning("MIDI input port '%s' is not working", port)
            return False
    else:
        try:
            open_input(port)
            log.info("MIDI input port '%s' is working", port)
            return True
        except:
            log.warning("MIDI input port '%s' is not working", port)
            return False
