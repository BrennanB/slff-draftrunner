# slff-draftrunner

## Setup

Download most recent python version from https://www.python.org/downloads/

__**When installing make sure you select "Add Python x.xx to PATH" (It's on the first page of the installer)**__
![image](https://i.imgur.com/RZTCCaK.png)

On the github page select the green button "Clone or Download" and download as a zip file. Extract your files.

Open your command line. For windows press Windows+R to open “Run” box. Type “cmd” and then click “OK” to open. In cmd type "pip install pandas" Leave it to run till successful messages appear.

You are now able to run the draft runner.

## Editing Settings

Right click "Settings.py" and edit with IDLE or your preferred text editor. Edit the variables as required.

### Settings Explanations

**ROUND_TIMING** - Each round in number of minutes

**START TIME** - [Hour starttime, minute starttime]

**SAVE_DIR** - Optional location for saving draft data

**OUTPUT_MODE** - Currently only works as "CD"

**RANDOM_ORDER** - True = Player order is randomized on draft creation, False = Order the teams are placed in during creation is maintained

**TIERS** - TRUE = If number of picks exceed number of pickable teams tiers will be created, FALSE = If number of picks exceed number of pickable teams duplicates of teams will be created.

## Updating

Re-download the ZIP file from Github, and update your save directory.

## Running a draft

Run "Draft Runner.py" file. Any commands you run, will auto copy the latest version of the draft to your clipboard. No need to copy the data. A preview will be shown of the draft and it's status, and all you need to do is verify the command ran, and then post the result into Chief Delphi

### Commands

Shortforms for each command will be denoted by (). [] denote values for the inputs. 

If you have enabled tiers preface each command with t(tier number)

#### pick (p) [team]

Selects a team for the active slot.

#### list (l) [player name]

Is case sensitive. Opens a text file for lists to be inputted.

#### random (r)

Randoms current slot

#### swap (s) [team out] [team in]

Swaps the two teams, will ask for clarification if multiple instances of the subbed out team exists. To clarify when prompted input the player name that is wanted.

#### print

Outputs current draft status.

#### delay [time delay minutes 1-59]

Delays the draft from 1-59 minutes. To delay more, run command multiple times.

#### exit/end/quit

Closes the draft runner.
