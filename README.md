# What is it?

**Eat Bacon** is an open-source toolset that provides ability to integrate
Beacon with OBS studio, in order to produce sport related content.

The tool are written in Python and LUA.

# License

Contents of this repository is licensed using MIT license. The license is
stored in `LICENSE.md` file.

You can also check [this](https://choosealicense.com/licenses/mit/) website.

# Beacon implementation

Tools used in this set are not using Beacon API as it's not publically
available. With reverse engineering I was able to get some data from Beacon
site and parse it to OBS-readable format. 

Please do not be angry - you know I love you :)

# Requirements

 * Python 3.10
 * Python-Pip
 * Python libraries from requirements.txt
 * Internet connection

# Preparing

In order to run this code, you need to have Python installed in correct version
with required packages. You can use pip and requirement.txt file in order to 
install packages, for example: `pip install -r requirements.txt`.

Editing `config.json` will allow you to:

 * Edit User Agent
 * Change sleep time (ignored in GUI mode)
 * Statuses naming
 * Modify outputs (see section below)

To run the app, you need execute it from the application directory.

# CLI mode
To run CLI mode, execute following command:
`python cli.py BEACON_ID`

Optionally `--config` argument can be provided to point into custom config
file or located in different location. Originally this file is located in 
the same directory as python script and named `config.json`.

The script is running in loop until Beacon returns 'Finished' or 'Unknown'
state. To finish execution earlier, please press `Ctrl+C` key combination.

# GUI mode

To run GUI mode, execute following command:
`python gui.py`

In GUI mode you cannot change `config.json` location. Inside the GUI
mode you can provide `BEACON_ID` and `Sleep` parameters.

# Modify outputs

Currently there are supported two types of outputs (excluding GUI mode):

* file - 5 txt files located in `out/` directory, each provides one parameter
* stdout - Shows nice message on stdout.

In order to disable/enable one output, you need to add/remove section
in the config file in "outout" section.

For `file` output, you can add `fn_prefix` that will change part of the
output filename. 