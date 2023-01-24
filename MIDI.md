
`ht-cli` should create a virtual MIDI input port as a control input.

Any input ports added to the `control: input:` section of the config file will also be opened as control inputs.

Values in `hacktribe_editor/midi_map.py` may need adjusting to suit your controller.

<br/>

Assuming an Akai MIDImix loaded with `midimix-preset.midimix`: 

Pots will control FX parameters 0..23, top to bottom, left to right.

Mute buttons will select channels 0..7, Rec Arm buttons will select channels 8..15.

Solo button will select MFX (channel 16).

Bank Right button will decrement FX control map index (0..10), Bank Left button will increment.

Fader 8 will set FX control map minimum value, fader 9 will set maximum value.

