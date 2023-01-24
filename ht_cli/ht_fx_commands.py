import logging
import json
import cloup
from cloup import option_group, option, OptionGroup
from cloup.constraints import mutually_exclusive, require_one
import click
from click_spinner import spinner
from ht_cli.ht_cli_utils import pass_hted
from hacktribe_editor import ht_fx_edit_utils as fxed_utils
from hacktribe_editor.ht_format import HtFXPreset
from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging

log = logging.getLogger(__name__)


def try_prompt(message, **kwargs):
    try:
        return click.prompt(message, **kwargs)
    except:
        print("\nValue required.\n")
        return None


chan_index_opt = option(
    '-c',
    '--channel',
    'chan_index',
    help="Channel index: [0..16] (16 == MFX)",
    is_flag=False,
    type=int,
    flag_value=(-1),
    metavar="INDEX",
)

ifx_index_opt = option(
    '-i',
    '--ifx',
    'ifx_index',
    help="IFX preset index: [0..95]",
    is_flag=False,
    type=int,
    flag_value=(-1),
    metavar="INDEX",
)

mfx_index_opt = option(
    '-m',
    '--mfx',
    'mfx_index',
    help="MFX preset index: [0..31]",
    is_flag=False,
    flag_value=(-1),
    type=int,
    metavar="INDEX",
)
src_file_path_opt = option(
    '-f',
    '--file',
    'file_path',
    type=cloup.Path(exists=True),
    help="Path to file.",
    is_flag=False,
    flag_value='',
    metavar="PATH",
)

dest_file_path_opt = option(
    '-f',
    '--file',
    'file_path',
    type=cloup.Path(),
    help="Path to file.",
    is_flag=False,
    flag_value='',
    metavar="PATH",
)

format_options = option_group(
    "Format",
    option(
        '-y',
        '--yaml',
        'yaml',
        is_flag=True,
    ),
    option(
        '-j',
        '--json',
        'json',
        is_flag=True,
    ),
    option(
        '-x',
        '--hex',
        'hex',
        is_flag=True,
    ),
    option(
        '-b',
        '--bytes',
        'bytes',
        is_flag=True,
    ),
    constraint=mutually_exclusive,
)

get_fx_src_options = option_group(
    'Source',
    chan_index_opt,
    ifx_index_opt,
    mfx_index_opt,
    constraint=require_one,
)

set_fx_src_options = option_group(
    'Source',
    chan_index_opt,
    src_file_path_opt,
    constraint=require_one,
)

set_fx_dest_options = option_group(
    "Destination",
    ifx_index_opt,
    mfx_index_opt,
    constraint=require_one,
)

dest_file_options = option_group(
    "Destination",
    dest_file_path_opt,
    constraint=require_one,
)

edit_fx_options = option_group(
    'Source',
    chan_index_opt,
    ifx_index_opt,
    mfx_index_opt,
    src_file_path_opt,
    constraint=require_one,
)
# ht_cli get fx ------------------------


@cloup.command(
    name='get',
    aliases=['g'],
    show_constraints=True,
    no_args_is_help=True,
)
@get_fx_src_options
@dest_file_options
@format_options
@pass_hted
@click.pass_context
@log_debug
def get_fx(ctx, hted, **params):
    '''
    Get FX preset at index from RAM.

    '''
    log.info('Called get_fx.')

    print("\nProcessing...")

    if params['chan_index'] is not None:

        if params['chan_index'] == (-1):
            params['chan_index'] = try_prompt("Source channel [0..16]",
                                              type=int)
            if params['chan_index'] is None:
                return

    elif params['ifx_index'] is not None:
        if params['ifx_index'] == (-1):
            params['ifx_index'] = try_prompt("Source IFX preset [0..95]",
                                             type=int)
            if params['ifx_index'] is None:
                return
        with spinner():
            preset = hted.ifxed.get_preset(params['ifx_index'])

    elif params['mfx_index'] is not None:
        with spinner():
            preset = hted.mfxed.get_preset(params['mfx_index'])

    if params['file_path'] == '':
        params['file_path'] = try_prompt("Destination file path")
        if params['file_path'] is None:
            return

    print("\nGet channel", params['chan_index'], "edit buffer as preset\n")
    with spinner():
        if params['chan_index'] == 16:
            preset = hted.mfxed.get_current_preset(params['chan_index'])
        else:
            preset = hted.ifxed.get_current_preset(params['chan_index'])

    print("\nWrite preset as", params['file_path'], "\n")
    log.warning("Preset naming not implemented yet.")

    # FIX - eww
    if params['bytes'] is not None or not any(
            k in params for k in ('hex', 'json', 'yaml')):
        with open(params['file_path'], 'wb') as f:
            f.write(preset.bytes)
    else:
        if params['yaml']:
            preset = preset.yaml
        elif params['json']:
            preset = preset.json
        elif params['hex']:
            preset = preset.hex

        with open(params['file_path'], 'w') as f:
            f.write(preset)

    print("\nDone!")


# ht_cli add fx --------------------------


@cloup.command(
    name='add',
    aliases=['a'],
    show_constraints=True,
    no_args_is_help=True,
)
@set_fx_src_options
@format_options
@pass_hted
@log_debug
def add_fx(hted, **params):
    ''' Add new FX preset to RAM. '''

    print("\nProcessing...")
    if params['file_path'] is not None:
        with open(params['file_path'], 'rb') as f:
            fx = f.read()

        if params['yaml']:
            preset = HtFXPreset.from_yaml(fx)
        elif params['json']:
            preset = HtFXPreset.from_json(fx)
        elif params['hex']:
            log.warning("HtFXPreset.from_hex() not implemented yet.")
            print("\nHtFXPreset.from_hex() not implemented yet.\n")
            return
        else:
            preset = HtFXPreset(fx)

        if fxed_utils.preset_is_mfx(preset.container):  # test if ifx or mfx
            log.warning("Add MFX preset not implemented yet.")
            print("\nAdd MFX preset not implemented yet.\n")
            return
        else:
            log.info("Add file as new IFX preset.")
            print("\nAdd file as new IFX preset.\n")
        with spinner():
            hted.ifxed.add_preset(preset)

    elif params['chan_index'] is not None:

        if params['chan_index'] == 16:
            mfx = True
            log.warning("Add MFX preset not implemented yet.")
            print("\nAdd MFX preset not implemented yet.\n")
            return
        else:
            preset = hted.ifxed.get_current_preset(params['chan_index'])
            log.info("Add channel edit buffer as new IFX preset.")
            print("\nAdd channel edit buffer as new IFX preset.\n")
            with spinner():
                hted.ifxed.add_preset(preset)

    print("\nDone!")


# ht_cli set fx --------------------------
@cloup.command(
    name='set',
    aliases=['s'],
    no_args_is_help=True,
)
@set_fx_src_options
@set_fx_dest_options
@pass_hted
@log_debug
def set_fx(hted, **params):
    '''
    Set FX preset at index in RAM.

    '''
    mfx = False

    print("\nProcessing...")
    with spinner():
        if params['file_path'] is not None:
            print("\nSet preset at index from file.\n")

            preset = HtFXPreset().from_file(params['file_path'])

            if params['mfx_index'] or fxed_utils.preset_is_mfx(
                    preset.dict):  # test if ifx or mfx
                mfx = True

        elif params['chan_index'] is not None:
            log.info("Set preset at index from channel edit buffer.")
            print("\nSet preset at index from channel edit buffer\n")

            if params['mfx_index'] or params['chan_index'] == 16:
                mfx = True
                preset = hted.mfxed.get_current_preset()
            else:
                preset = hted.ifxed.get_current_preset(params['chan_index'])
        if mfx:
            fx_index = params['mfx_index']
            hted.mfxed.set_preset(fx_index, preset)
        else:
            fx_index = params['ifx_index']
            hted.ifxed.set_preset(fx_index, preset)
    print("\nDone!")


# ht_cli show fx --------------------------


@cloup.command(
    name='show',
    aliases=['v', 'sh'],
    no_args_is_help=True,
)
@edit_fx_options
@format_options
@pass_hted
@log_debug
def show_fx(hted, **params):
    '''Show FX properties.'''
    log.info("Called show_fx.")

    print("\nProcessing...")
    with spinner():

        if params['ifx_index'] is not None:
            log.info("Received option '--ifx %s'.", params['ifx_index'])
            fx = hted.ifxed.get_preset(params['ifx_index'])

        elif params['mfx_index'] is not None:
            log.info("Received option '--mfx %s'.", params['mfx_index'])
            fx = hted.mfxed.get_preset(params['mfx_index'])

        elif params['chan_index'] is not None:
            log.info("Received option '--channel %s'.", params['chan_index'])

            if params['chan_index'] == 16:
                fx = hted.mfxed.get_current_preset()
            else:
                fx = hted.ifxed.get_current_preset(params['chan_index'])

        elif params['file_path'] is not None:
            log.info("Received option '--file %s'.", params['file_path'])
            with open(params['file_path'], 'rb') as f:
                fx = HtFXPreset(f.read())

        if params['bytes']:
            print(''.join('\\x{:02x}'.format(b) for b in fx.bytes))
        elif params['json']:
            print(json.dumps(json.loads(fx.json), indent=4))
        elif params['yaml']:
            print(fx.yaml)
        elif params['hex']:
            print(fx.hex)

        else:
            print(fx.yaml)

    print("\nDone!")


# ht_cli edit fx --------------------------


@cloup.command(
    name='edit',
    aliases=['e'],
    no_args_is_help=True,
)
@edit_fx_options
@format_options
@pass_hted
@log_debug
def edit_fx(hted, **params):
    '''Edit FX properties.'''
    log.info("Called edit_fx.")

    print("Processing...")

    if params['ifx_index'] is not None:
        log.info("Received option '--ifx %s'.", params['ifx_index'])
        fx = hted.ifxed.get_preset(params['ifx_index'])
        if params['hex']:
            fxx = click.edit(fx.bytes, editor='hexedit', require_save=False)
            with spinner():
                hted.ifxed.set_preset(params['ifx_index'],
                                      HtFXPreset.from_bytes(fxx))
        else:
            fxy = click.edit(fx.yaml, require_save=False)
            with spinner():
                hted.ifxed.set_preset(params['ifx_index'],
                                      HtFXPreset.from_yaml(fxy))

    elif params['mfx_index'] is not None:
        log.info("Received option '--mfx %s'.", params['mfx_index'])
        fx = hted.mfxed.get_preset(params['mfx_index'])
        fxy = click.edit(fx.yaml, require_save=False)
        with spinner():
            hted.mfxed.set_preset(params['mfx_index'],
                                  HtFXPreset.from_yaml(fxy))

    elif params['chan_index'] is not None:
        log.info("Received option '--channel %s'.", params['chan_index'])
        if params['chan_index'] == 16:
            fx = hted.mfxed.get_current_preset()
            fxy = click.edit(fx.yaml, require_save=False)
            with spinner():
                hted.mfxed.add_preset(HtFXPreset.from_yaml(fxy))
        else:
            fx = hted.ifxed.get_current_preset(params['chan_index'])
            fxy = click.edit(fx.yaml, require_save=False)
            with spinner():
                hted.ifxed.add_preset(HtFXPreset.from_yaml(fxy))

    elif params['file_path'] is not None:
        log.info("Received option '--file %s'.", params['file_path'])
        with open(params['file_path'], 'rb') as f:
            fx = HtFXPreset(f.read())
        if params['hex']:
            fxx = click.edit(fx.bytes, editor='hexedit', require_save=False)
            with open(params['file_path'], 'wb') as f:
                f.write(HtFXPreset.from_bytes(fxx).bytes)
        else:
            fxy = click.edit(fx.yaml, require_save=False)
            with open(params['file_path'], 'wb') as f:
                f.write(HtFXPreset.from_yaml(fxy).bytes)

    print("\nDone!")
