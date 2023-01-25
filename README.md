# Hacktribe Editor

## ht-cli

Early support for FX editing.

<br/>

### Testing

Clone the repo and enter directory:


    git clone --recursive -b ht-cli https://bangcorrupt/hacktribe-editor
    cd hacktribe-editor

<br/>

Create and activate virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

<br/>

Install:

    pip install .

<br/>

Run `ht-cli` with no options to enter an interactive prompt:

    ht-cli

You should see:

    ________________________________________
    _  _ ____ ____ _  _ ___ ____ _ ___  ____ 
    |__| |__| |    |_/   |  |__/ | |__] |___ 
    |  | |  | |___ | \_  |  |  \ | |__] |___ 
                                             
    https://github.com/bangcorrupt/hacktribe
    ________________________________________


         Welcome to Hacktribe Editor.

      Run 'help' to see available options.

     Run 'control' to initialise Hacktribe.
     
    [ ht ] 


<br/>


At the `[ ht ]` prompt, run `help` to show some help.  You should see something like:


    [ ht ] help
    Usage: ht-cli  help [OPTIONS] COMMAND [ARGS]...

      Command line interface for Hacktribe Editor.

    Options:
      -l, --log [d|debug|i|info|w|warning|e|error|c|critical]
                  Log level.
      -h, --help  Show this message and exit.

    Commands:
      about (ab)                   All about Hacktribe Editor.
      config (c, cfg, conf)        Configure Hacktribe Editor.
      control (r, run, ctl, ctrl)  Control Hacktribe Editor.
      fx (f, efx, effects)         FX commands.
      help (h, ?)                  Show help message for [command].

<br/>


In the prompt, we can hit tab and space to auto-complete commands.

There isn't a lot of console feedback yet, 

so set the log level to `INFO` to see what's happening:


    config debug --log info

You should see a log message for most function calls.

If it's too much information, set the log level to `ERROR`. 


<br/>


Configure Hacktribe MIDI input:

    config midi -i


You should get a prompt with a list of available electribe MIDI ports.

<br/>

Likewise for Hacktribe MIDI output:

    config midi -o

<br/>


Configure a MIDI control input (optional):

    config midi -c

You should get a prompt with a list of available MIDI ports, choose one that isn't Hacktribe.

See MIDI.md for more information on MIDI mapping.  


<br/>

Run `control` to initialise MIDI communication with Hacktribe.

The log output should include the line:

    INFO    [ht_editor.py:ht_editor:init_midi:130] MIDI initialisation succeeded.


<br/>

Show the FX settings for channel 0:

    fx show -c 0


This should print some yaml to the console.

<br/>


Get the current settings of channel 0 FX as a preset file:

    fx get -c 0 -f my-preset.ifx

<br/>

Edit an FX preset file:

    fx edit -f my-preset.ifx

This should open the file in yaml format in your default text editor.


Edit the `name` field to something more interesting and save the file.

<br/>

Add a new IFX preset to Hacktribe:

    fx add -f my-preset.ifx


The Hacktribe screen will start flashing 'Working' like crazy.  

After a while it will stop and you should see your new IFX preset at the top of the list.

<br/>

Setting an existing FX preset is a little quicker:

    fx set -m 31 -f ht_data/fx/wet-plate-reverb.mfx

You should see the Autopan MFX has been replaced with a new plate reverb.


<br/>

Read through the help in the cli and try stuff out.  Have a look in `ht_data/fx` for some presets.

This tool only acts on the CPU RAM, so if everything goes wrong reboot Hacktribe.

More documentation coming soon.

<br/>

### Issues

Many features not implemented yet.

For stereo samples select second channel of pair.

Please use the Hacktribe Editor discussion forum before opening a new issue.

If it crashes, please include `ht_editor.log` as an attachement (please don't paste the contents, there is a lot of it).
