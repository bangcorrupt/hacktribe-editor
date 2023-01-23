# Hacktribe Editor

## ht-cli

Early support for FX editing.

<br/>

### Testing

Clone the repo and enter directory:
    
    git clone --recursive -b ht-cli https://bangcorrupt/hacktribe-editor
    cd hacktribe-editor

<<<<<<< HEAD
<br/>
=======
>>>>>>> 5f0782f (readme)

Create and activate virtual environment:

    python3 -m venv venv
    source venv/bin/activate

<<<<<<< HEAD
<br/>
=======
>>>>>>> 5f0782f (readme)

Install:

    pip install .

<<<<<<< HEAD
<br/>
=======
>>>>>>> 5f0782f (readme)

Run:

    ht-cli

<<<<<<< HEAD
<br/>
=======
>>>>>>> 5f0782f (readme)

Enter an interactive prompt:

    ht-cli repl

<br/>

Show some help:

    --help

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

<<<<<<< HEAD
You should get a prompt with a list of available MIDI ports.  Choose one that isn't Hacktribe.
=======

You should get a prompt with a list of available MIDI ports.  Choose one that isn't Hacltribe.
>>>>>>> 5f0782f (readme)

If you have an Akai MIDImix, load it with `midimix-preset.midimix`.  

If not, adjust the values in `hacktribe_editor/midi_map.py` to suit your controller.

Assuming a MIDImix, pots will control FX parameters 0..23, top to bottom, left to right.

Mute buttons will select channels 0..7, Rec Arm buttons will select channels 8..15.

Solo button will select MFX (channel 16).

Bank Right button will decrement FX control map index (0..10), Bank Left button will increment.

Fader 8 will set FX control map minimum value, fader 9 will set maximum value.

<br/>

Show the FX settings for channel 0:

    show fx -c 0


This should print some yaml to the console

<br/>


Get the current settings of channel 0 FX as a preset file:

    get fx -c 0 -f my-preset.ifx

<br/>

Edit an FX preset file:

    edit fx -f my-preset.ifx

<<<<<<< HEAD
This should open the file in yaml format in your default text editor.
=======

This should the file in yaml format in your default text editor.
>>>>>>> 5f0782f (readme)

Edit the `name` field to something more interesting and save the file.

<br/>

Add a new IFX preset to Hacktribe:

    add fx -f my-preset.ifx


The screen will start flashing 'Working' like crazy.  

After a while it will stop and you should see your new IFX preset at the top of the list.

<br/>

Setting an existing FX preset is a little quicker:

    set fx -m 31 -f ht_data/fx/wet-plate-reverb.mfx

<<<<<<< HEAD
You should see the Autopan MFX has been replaced with new plate reverb.
=======

You should see the 'Punch' IFX has been replaced with your awesome new preset.
>>>>>>> 5f0782f (readme)

<br/>

Read through the help in the cli and try stuff out.  Have a look in `ht_data/fx` for some presets.

This tool only acts on the CPU RAM, so if everything goes wrong reboot Hacktribe.

More documentation comming soon.

<<<<<<< HEAD
<br/>
=======
>>>>>>> 5f0782f (readme)

### Issues

Many features not implemented yet.

For stereo samples select second channel of pair.

<<<<<<< HEAD
Please use the Hacktribe Editor discussion forum before opening a new issue.

If it crashes, please include `ht_editor.log` as an attachement (please don't paste the contents, there is a lot of it).
=======
Please use the Hacktribe Editor discussion forum before opening an issue.
>>>>>>> 5f0782f (readme)
