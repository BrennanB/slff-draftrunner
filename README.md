# slff-draftrunner

## Setup

Download most recent python version from https://www.python.org/downloads/

__**When installing make sure you select "Add Python x.xx to PATH"**__

On the github page select the green button "Clone or Download" and download as a zip file. Extract your files.

Open your command line. For windows press Windows+R to open “Run” box. Type “cmd” and then click “OK” to open. In cmd type "pip install pandas" Leave it to run till successful messages appear.

Create a folder for where you would like the draft data to be saved. Copy the location of that folder. If you move this folder, you will have to re-update this location. 

Right click "Draftrunner.py" and edit with IDLE or your preferred text editor. Edit the variable "SAVE_DIR" to your new location and save.

You are now able to run the draft runner.

## Updating

Re-download the ZIP file from Github, and update your save directory.

## Running a draft

Run "Draft Runner.py" file

### Commands

Shortforms for each command will be denoted by (). [] denote values for the inputs. If you have enabled tiers preface each command with t(tier number)

#### pick (p) [team]

Selects a team for the active slot.

#### list (l) [player name]

Is case sensitive. Opens a text file for lists to be inputted.

#### random (p)

Randoms current slot

#### swap (s) [team out] [team in]

Swaps the two teams, will ask for clarification if multiple instances of the subbed out team exists. To clarify when prompted input the player name that is wanted.

#### print

Outputs current draft status.

#### exit/end/quit

Closes the draft runner.
