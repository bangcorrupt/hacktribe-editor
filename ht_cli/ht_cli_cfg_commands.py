import logging
from pathlib import Path

import cloup
from cloup import option, option_group
from cloup.constraints import mutually_exclusive, require_one, require_any

from ht_cli.ht_cli_utils import pass_hted, test_port, prompt_ports
from hacktribe_editor.ht_logging import log_debug
import hacktribe_editor.ht_logging

log = logging.getLogger(__name__)

# ht_cli config midi ---------------------


@cloup.command(
    name='midi',
    aliases=['m', 'mi', 'mid'],
    no_args_is_help=True,
)
@option_group(
    "MIDI Options",
    option(
        '-i',
        '--input',
        'input_port',
        prompt=prompt_ports('tribe'),
        prompt_required=False,
        help="Set input port.",
        metavar="'PORT_NAME'",
    ),
    option(
        '-o',
        '--output',
        'output_port',
        prompt=prompt_ports('tribe', output=True),
        prompt_required=False,
        help="Set output port.",
        metavar="'PORT_NAME'",
    ),
    option(
        '-c',
        '--control',
        'control_port',
        prompt=prompt_ports(),
        prompt_required=False,
        help="Set control port.",
        metavar="'PORT_NAME'",
    ),
    option('-m',
           '--map',
           'midi_map',
           default=None,
           help="Not implemented yet.",
           metavar="PATH"),
    option(
        '-l',
        '--list',
        'list_ports',
        is_flag=True,
        help="Not implemented yet.",
    ),
    constraint=require_any,
)
@pass_hted
@log_debug
def config_midi(hted, input_port, output_port, control_port, midi_map,
                list_ports):
    ''' Configure MIDI. '''
    log.info('Called cli.config.midi.')

    if input_port is not None:
        log.info("Received option input_port='%s'.", input_port)
        if test_port(input_port):
            msg = "\nInput port is working, configuration updated.\n"

            hted.config['midi']['input'] = input_port
            hted.init_midi()
            if hted.auto_write_config:
                hted.write_config()
            print(msg)
            log.info(msg)
        else:
            msg = "\nInput port is not working, configuration not changed.\n"
            print(msg)
            log.warning(msg)

    if output_port is not None:
        log.info("Received option output_port='%s'.", output_port)
        if test_port(output_port, output=True):
            msg = "\nOutput port is working, configuration updated.\n"

            hted.config['midi']['output'] = output_port
            if hted.auto_write_config:
                hted.write_config()
            print(msg)
            log.info(msg)
        else:
            msg = "\nOutput port is not working, configuration not changed.\n"
            print(msg)
            log.warning(msg)

    if control_port is not None:
        log.info("Received option control_port='%s'.", control_port)
        if test_port(control_port):
            msg = "\nControl port is working, configuration updated.\n"

            # ADD - handle multiple control inputs
            hted.config['midi']['control']['input'].append(control_port)
            if hted.auto_write_config:
                hted.write_config()
            print(msg)
            log.info(msg)
        else:
            msg = "\nControl port is not working, configuration not changed.\n"
            print(msg)
            log.warning(msg)


# ht_cli config path ----------------------


@cloup.argument('path')
@cloup.command(
    name='path',
    aliases=['p', 'dir'],
    show_constraints=True,
    no_args_is_help=True,
)
@pass_hted
@log_debug
def config_path(hted, **params):
    '''
    Set data directory.

    PATH is /path/to/directory
    '''
    log.info("Called cli.config.path.")
    hted.config['path'] = str(Path(params['path']))
    if hted.auto_write_config:
        hted.write_config()
