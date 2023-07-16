# Hacktribe Editor

An editor app for hacktribe

## Features
 - GUI
 - Patch firmware

<br/>

To test:

Clone Hacktribe Editor including submodules:

    git clone --recursive https://github.com/bangcorrupt/hacktribe-editor.git

Enter `hacktribe-editor` directory:

    cd hacktribe-editor

Install dependencies:

    pip install -r requirements.txt

<br/>

Copy factory firmware to `hacktribe-editor/hacktribe/SYSTEM.VSB`.

<br/>

Run `hacktribe_app_gui.py`:

    python hacktribe_app_gui.py

Follow the instructions in the app, pay attention to the log output in the text box.

<br/>

Installation of bsdiff4 will fail on Windows without the correct build tools installed, see [#103](https://github.com/bangcorrupt/hacktribe/issues/103).

In that case, run the [executable](https://github.com/bangcorrupt/hacktribe-editor/blob/main/hacktribe-gui.exe) found at hacktribe-editor/hacktribe-gui.exe.


