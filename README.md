# slff-draftrunner

## Setup

Download most recent python version from https://www.python.org/downloads/

__**When installing make sure you select "Add Python x.xx to PATH" (It's on the first page of the installer)**__
![image](https://i.imgur.com/RZTCCaK.png)

On the github page select the green button "Clone or Download" and download as a zip file. Extract your files.

Open your command line. For windows press Windows+R to open “Run” box. Type “cmd” and then click “OK” to open. In cmd type "pip install pandas" Leave it to run till successful messages appear.

In cmd type "pip install gspread"

In cmd type "pip install gspread_dataframe"

In cmd type "pip install oauth2client"

Create a google sheets api key, or SLFF draft runners can recieve one from me.

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

**ROOKIE_CUTOFF** - Insert the lowest number rookie of the year here.

## Updating

Re-download the ZIP file from Github, and update your save directory.

## Running a draft

Run "Draft Runner.py" file. 

A .txt file will automatically open to ask for the player list (the people who are making picks). Paste your player list in the txt file, close and save.

Another .txt file will open for your team list (actual FRC teams). Paste your team list, close and save.

The draft runner will now generate a draft based on the settings you set in settings.py. If you enabled tiers, and tiers were required, you will need to use the "print" command to view each tier by using the tier prefix, and then print command.

Any commands you run, will auto copy the latest version of the draft to your clipboard. No need to copy the data. A preview will be shown of the draft and it's status, and all you need to do is verify the command ran, and then post the result into Chief Delphi.

To add a list, use the list command, the next available team will automatically be put into the team's pick slot when it is thier turn.
Teams will also automatically be randomed if they had been randomed previously by the draft runner. All of this is done by the team's status in the draft runner output.

To re-enable a list, use the list command for the specified team, and save and close the list.

If a player is no longer mia, and would like to not be randomed for next round, swap in and out their randomed team to take them off of the auto random cycle (Better solution coming sometime)

After each pick, the draft runner will update the current SLFF year sheet, and post the results that it has, as they get updated.

If you need to do any modification to the team list/player list/random list, you will need to find the event files in your set save directory (defaults into the folder where draft runner.py is) and modify the .json and .txt files accordingly.

Since all the lists and mia randoming are done automatically based on the "Status" column, you may find some times where you wish to change a players status manually. One use case is a quicker method of re-enabling a list. To do so, use the status command.

Inserting "rookie" or "rookies" in a list, will automatically give you the highest rookie number on the random list.

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

#### status [player name] [status to change to]

Changes a player's status in the status column:

Use the following commands for changing

mia = *MIA*

live = *Live Picking*

missing = *Missing*

list = *list*

#### remaining

Posts the remaining teams available for a draft that went unpicked. Useful for setting up multi day drafts.

#### exit/end/quit

Closes the draft runner.
