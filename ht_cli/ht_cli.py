#!/usr/bin/env python
import logging
from pathlib import Path

import click
import cloup
from cloup import HelpFormatter, HelpTheme, Style, option_group, option
from cloup.constraints import require_one
from click_repl import repl
from prompt_toolkit.history import FileHistory
from pyfiglet import Figlet

from hacktribe_editor import ht_logging
from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor.ht_editor import HacktribeEditor
from hacktribe_editor.ht_control import HtControl
from ht_cli.ht_fx_commands import get_fx, set_fx, add_fx, show_fx, edit_fx
from ht_cli.ht_cli_cfg_commands import config_midi, config_path
from ht_cli.ht_cli_utils import pass_hted

# Reduce log spam
logging.getLogger('asyncio').setLevel(logging.ERROR)

log = logging.getLogger(__name__)
log.info('Starting ht_cli.')

# ht_cli -----------------------------------

theme = HelpTheme(
    invoked_command=Style(fg='bright_yellow'),
    heading=Style(fg='bright_white', bold=True),
    constraint=Style(fg='magenta'),
    col1=Style(fg='bright_yellow'),
)
dark_theme = HelpTheme.dark()
light_theme = HelpTheme.light()
no_theme = HelpTheme()

help_theme = theme

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    formatter_settings=HelpFormatter.settings(theme=help_theme),
)


@cloup.group(
    context_settings=CONTEXT_SETTINGS,
    show_subcommand_aliases=True,
    invoke_without_command=True,
    no_args_is_help=True,
)
@cloup.option(
    '-l',
    '--log',
    'log_level',
    default=None,
    prompt=True,
    prompt_required=False,
    is_eager=True,
    type=click.Choice([
        'd',
        'debug',
        'i',
        'info',
        'w',
        'warning',
        'e',
        'error',
        'c',
        'critical',
    ],
                      case_sensitive=False),
    help="Log level.",
)
@pass_hted
@log_debug
def cli(hted=None, log_level=None):
    ''' Command line interface for Hacktribe Editor. '''
    log.info("Called cli.")

    if log_level is not None:
        if log_level == 'd':
            log_level = 'debug'
        elif log_level == 'w':
            log_level = 'warning'
        elif log_level == 'i':
            log_level = 'info'
        elif log_level == 'e':
            log_level = 'error'
        elif log_level == 'c':
            log_level = 'critical'
        ht_logging.set_log_level(log_level)
    else:
        ht_logging.set_log_level(hted.config['log']['level'])


@cli.command(
    name='repl',
    aliases=['re', 'rep'],
    help="Enter an interactive prompt.",
)
@pass_hted
@log_debug
def ht_repl(hted):
    prompt_kwargs = {
        'history': FileHistory(Path('./ht-cli.history')),
    }

    print_banner()
    # Initialise MIDI control
    HtControl(hted)
    repl(click.get_current_context(), prompt_kwargs=prompt_kwargs)


# ht_cli about ------------------------------


@cli.command(
    name='about',
    aliases=['ab'],
    help='All about Hacktribe Editor.',
)
@pass_hted
@log_debug
def about(hted):

    print_banner()


# ht_cli config -----------------------------


@cli.group(
    name='config',
    aliases=['c', 'cfg', 'conf'],
    show_subcommand_aliases=True,
    no_args_is_help=True,
)
@pass_hted
@log_debug
def config_group(hted):
    ''' Configure Hacktribe Editor. '''
    log.info("Called cli.config_group.")


@cloup.command(
    name='debug',
    aliases=['d', 'deb', 'dbg'],
    no_args_is_help=True,
)
@option_group(
    "Debug Options",
    require_one(
        option(
            '-l',
            '--log',
            'log_level',
            default='debug',
            prompt=True,
            prompt_required=False,
            type=click.Choice([
                'd',
                'debug',
                'i',
                'info',
                'w',
                'warning',
                'e',
                'error',
                'c',
                'critical',
            ],
                              case_sensitive=False),
            help="Log level",
        ), ),
)
@pass_hted
@log_debug
def config_debug(hted, log_level):
    ''' Configure debugging. '''
    log.info('Called cli.debug.')
    if log_level == 'd':
        log_level = 'debug'
    if log_level == 'w':
        log_level = 'warning'
    if log_level == 'i':
        log_level = 'info'
    if log_level == 'e':
        log_level = 'error'
    if log_level == 'c':
        log_level = 'critical'
    ht_logging.set_log_level(log_level)
    hted.config['log']['level'] = log_level
    if hted.auto_write_config:
        hted.write_config()


config_group.add_command(config_midi)
config_group.add_command(config_path)
config_group.add_command(config_debug)

# ht_cli control ----------------------------


# ADD - option to send SysEx/NRPN
@cli.command(
    aliases=['r', 'run', 'ctl', 'ctrl'], )
@pass_hted
@log_debug
def control(hted):
    ''' Control Hacktribe Editor. '''
    log.info("Called cli.control.")
    # Initalise realtime control if not already running
    HtControl(hted)


# ht_cli get -----------------------------


@cli.group(
    name='get',
    aliases=['g', 'ge'],
    show_subcommand_aliases=True,
    no_args_is_help=True,
)
@pass_hted
@log_debug
def get_group(hted):
    ''' Get something. '''
    log.info("called cli.get_group")


get_group.add_command(get_fx)

# ht_cli set -----------------------------


@cli.group(
    name='set',
    aliases=['s', 'se'],
    show_subcommand_aliases=True,
    no_args_is_help=True,
)
@pass_hted
@log_debug
def set_group(hted):
    ''' Set something.'''
    log.info("called cli.set_group")


set_group.add_command(set_fx)

# ht_cli add -----------------------------


@cli.group(
    name='add',
    aliases=['a', 'ad'],
    show_subcommand_aliases=True,
    no_args_is_help=True,
)
@pass_hted
@log_debug
def add_group(hted):
    ''' Add something. '''
    log.info("called cli.add_group")


add_group.add_command(add_fx)

# ht_cli show ----------------------------


@cli.group(
    'show',
    aliases=['sh'],
    show_subcommand_aliases=True,
    no_args_is_help=True,
)
@pass_hted
@log_debug
def show_group(hted):
    ''' Show something.'''
    log.info("called cli.show_group")


show_group.add_command(show_fx)

# ht_cli list ----------------------------


@cli.group(
    name='list',
    aliases=['l', 'ls'],
    show_subcommand_aliases=True,
    no_args_is_help=True,
)
@pass_hted
@log_debug
def list_group(hted):
    ''' List some things.'''
    log.info("called cli.list_group")


# list_group.add_command(list_fx)

# ht_cli edit ----------------------------


@cli.group(
    name='edit',
    aliases=['e', 'ed'],
    show_subcommand_aliases=True,
    no_args_is_help=True,
)
@pass_hted
@log_debug
def edit_group(hted):
    ''' Edit something.'''
    log.info("called cli.edit_group")


edit_group.add_command(edit_fx)


# ht_cli get fx --------------------------
def print_banner():
    fig = Figlet(font='cybermedium')
    title = fig.renderText("Hacktribe")
    line = '_' * 40 + "\n"
    link = "https://github.com/bangcorrupt/hacktribe\n"
    banner = line + title + link + line

    click.echo(click.style(
        banner,
        fg="red",
        bold=True,
    ))


if __name__ == '__main__':
    cli()
