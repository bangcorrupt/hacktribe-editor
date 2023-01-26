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

in_repl = False


@cloup.group(
    context_settings=CONTEXT_SETTINGS,
    show_subcommand_aliases=True,
    invoke_without_command=True,
    name='cli',
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
@click.pass_context
@log_debug
def cli(ctx, hted=None, log_level=None):
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

    if ctx.invoked_subcommand is None:
        print_banner()
        # Initialise MIDI control
        # HtControl(hted)
        global in_repl
        in_repl = True

        leave = False
        while not leave:
            leave = True
            prompt_kwargs = {
                'history': FileHistory(Path('./ht-cli.history')),
                'message': '[ ht ] '
            }
            try:
                repl(
                    ctx,
                    prompt_kwargs=prompt_kwargs,
                )
            except Exception:
                log.error("Exception.")

            leave = click.confirm('Exit ht-cli?', default=True)


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


@cloup.group(
    name='fx',
    aliases=['f', 'efx', 'effects'],
    show_subcommand_aliases=True,
    invoke_without_command=True,
)
@pass_hted
@click.pass_context
@log_debug
def fx_group(ctx, hted):
    ''' FX commands.'''
    log.info("called cli.fx_group")

    prompt_kwargs = {
        'history': FileHistory(Path('./ht-cli.history')),
        'message': '[ ht.fx ] '
    }
    if ctx.invoked_subcommand is None:
        if in_repl:
            # Initialise MIDI control
            # HtControl(hted)

            repl(
                ctx,
                prompt_kwargs=prompt_kwargs,
                allow_nested_groups=True,
            )

        else:
            print_help(ctx.command)


fx_group.add_command(add_fx, name='add')
fx_group.add_command(set_fx, name='set')
fx_group.add_command(get_fx, name='get')
fx_group.add_command(show_fx, name='show')
fx_group.add_command(edit_fx, name='edit')
fx_group.add_command(config_group)

cli.add_command(fx_group)


@cloup.command(
    name='help',
    aliases=['h', '?'],
    help="Show help message for [command].",
)
@pass_hted
@click.pass_context
@cloup.argument('cmd', required=False, help="Optional command name.")
@log_debug
def get_help(ctx, hted, cmd=None):
    ''' Show help message for command. '''
    if cmd is not None:
        print_help(ctx.parent.command.get_command(ctx, cmd))
    else:
        print_help(ctx.parent.command)


cli.add_command(get_help)
fx_group.add_command(get_help)


def print_help(command):
    ctx = click.get_current_context()
    click.echo(command.get_help(ctx))


def print_banner():
    fig = Figlet(font='cybermedium')
    title = fig.renderText("Hacktribe")
    line = '_' * 40 + "\n"
    link = "https://github.com/bangcorrupt/hacktribe\n"

    intro = "\n     Welcome to Hacktribe Editor.\n" \
            "\n  Run 'help' to see available options.\n" \
            "\n Run 'control' to initialise Hacktribe.\n"

    banner = line + title + link + line

    click.echo(click.style(
        banner,
        fg="red",
        bold=True,
    ))

    click.echo(click.style(
        intro,
        fg="green",
        bold=True,
    ))


if __name__ == '__main__':
    cli()
