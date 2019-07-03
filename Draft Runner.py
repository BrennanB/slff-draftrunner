import random
import os
import json
import pandas as pd
import math
import re
import Draft

# SETTINGS

ROUND_TIMING = [2, 1, 1]
START_TIME = [8, 0]
SAVE_DIR = r"C:\Users\brenn\Desktop\Runner Data"
OUTPUT_MODE = "CD"
RANDOM_ORDER = True
TIERS = True


# TODO Add a rookie random function
# TODO Tier support


# CREATE DIRECTORY
start_draft = True
while start_draft is True:
    event_name = input("What is your Event Name?: ")
    if "'" in event_name:
        print("The character ' is not permitted in event names")
    else:
        if os.path.isdir("{}\{}".format(SAVE_DIR, event_name)):
            correct_prompt = input("Looks like this event exists already! Would you like to load the data? [Y/N]: ")
            if correct_prompt.lower() == "y":
                start_draft = False
                loading = True
            else:
                print("Please try again!")
        else:
            os.mkdir("{}\{}".format(SAVE_DIR, event_name))
            start_draft = False
            loading = False
        base_path = "{}\{}".format(SAVE_DIR, event_name)

players_input = "{}\Players.txt".format(base_path)
teams_input = "{}\Teams.txt".format(base_path)
players_data_location = "{}\Players.json".format(base_path)
teams_data_location = "{}\Teams.json".format(base_path)
random_list_location = "{}\Randoms.json".format(base_path)

if loading is True:
    print("Loaded data")
    with open(players_data_location) as json_file:
        players_clean = json.load(json_file)
    with open(teams_data_location) as json_file:
        teams_clean = json.load(json_file)
    with open(random_list_location) as json_file:
        random_teams = json.load(json_file)
else:
    # INITIALIZE DRAFT SETTINGS

    # Input Players
    f = open(players_input, "w")
    f.close()
    fd = os.system("notepad.exe {}".format(players_input))
    f = open(players_input, "r")
    players = f.readlines()
    players_clean = [x.replace('\n', '') for x in players]
    players_clean = list(filter(None, players_clean))
    if RANDOM_ORDER:  # If random order setting is activated.
        random.shuffle(players_clean)
    with open(players_data_location, 'w') as outfile:
        json.dump(players_clean, outfile)

    # Input Teams
    f = open(teams_input, "w")
    f.close()
    df = os.system("notepad.exe {}".format(teams_input))
    f = open(teams_input, "r")
    teams = f.readlines()
    teams_clean = [x.replace('\n', '') for x in teams]

    random_teams = [x.replace('\n', '') for x in teams]
    random.shuffle(random_teams)
    with open(teams_data_location, 'w') as outfile:
        json.dump(teams_clean, outfile)
    with open(random_list_location, 'w') as outfile:
        json.dump(random_teams, outfile)

tier_ratio = math.ceil(len(players_clean) / (len(teams_clean) / len(ROUND_TIMING)))
base_team_list = teams_clean.copy()
available_team_list = []
for team in base_team_list:
    available_team_list.append([team, tier_ratio])

Draft.run_draft(START_TIME, base_path,tier_ratio, ROUND_TIMING, RANDOM_ORDER, OUTPUT_MODE, players_clean, available_team_list, random_teams, teams_clean)