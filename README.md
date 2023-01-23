# Hacktribe Editor

## ht-cli

Early support for FX editing.

### Testing

Clone the repo and enter directory:
    
    git clone --recursive -b ht-cli https://bangcorrupt/hacktribe-editor
    cd hacktribe-editor

Create and activate virtual environment:

    python3 -m venv venv
    source venv/bin/activate

Install:

    pip install .

Run:

    ht-cli

Enter an interactive prompt:

    ht-cli repl


Show some help:

    --help


Configure Hacktribe MIDI input:

    config midi -i

You should get a prompt with a list of available electribe MIDI ports.

Likewise for Hacktribe MIDI output:

    config midi -o


Configure a MIDI control input (optional):

    config midi -c

You should get a prompt with a list of available MIDI ports.  Choose one that isn't Hacktribe.

If you have an Akai MIDImix, load it with `midimix-preset.midimix`.  

If not, adjust the values in `hacktribe_editor/midi_map.py` to suit your controller.

Assuming a MIDImix, pots will control FX parameters 0..23, top to bottom, left to right.

Mute buttons will select channels 0..7, Rec Arm buttons will select channels 8..15.

Solo button will select MFX (channel 16).

Bank Right button will decrement FX control map index (0..10), Bank Left button will increment.

Fader 8 will set FX control map maximum value, fader 9 will set minimum value.


Show the FX settings for channel 0:

    show fx -c 0

This should print some yaml to the console


Get the current settings of channel 0 FX as a preset file:

    get fx -c 0 -f my-preset.ifx


Edit an FX preset file:

    edit fx -f my-preset.ifx

This should open the file in yaml format in your default text editor.

Edit the `name` field to something more interesting and save the file.


Add a new IFX preset to Hacktribe:

    add fx -f my-preset.ifx

The screen will start flashing 'Working' like crazy.  

After a while it will stop and you should see your new IFX preset at the top of the list.


Setting an existing FX preset is a little quicker:

    set fx -m 31 -f ht_data/fx/wet-plate-reverb.mfx

You should see the Autopan MFX has been replaced with new plate reverb.


Read through the help in the cli and try stuff out.  Have a look in `ht_data/fx` for some presets.

This tool only acts on the CPU RAM, so if everything goes wrong reboot Hacktribe.

More documentation comming soon.

### Issues

Many features not implemented yet.

For stereo samples select second channel of pair.

Please use the Hacktribe Editor discussion forum before opening a new issue.
