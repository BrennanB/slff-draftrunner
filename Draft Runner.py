import random
import os
import json
import math
import draft
from discourse import DiscourseClient
import secrets

client = DiscourseClient('https://chiefdelphi.com', api_username=secrets.DISCOURSE_USERNAME, api_key=secrets.DISCOURSE_KEY)

user = client.user('BrennanB')
client.send_pm('BrennanB', "Test PM", "This is a test message")
# print(user)

# SETTINGS

ROUND_TIMING = [2, 2, 2]
START_TIME = [8, 0]
SAVE_DIR = r"E:\_Python Projects\Draft Runner Data"
OUTPUT_MODE = "CD"
RANDOM_ORDER = True
TIERS = True

# TODO Add a rookie random function


def get_tier_sizes(num_players, num_teams, num_picks=3):
    tiers = math.ceil(num_players / math.floor(num_teams / num_picks))
    current_size = math.floor(num_players / tiers)
    tier_sizes = []

    while num_players > current_size:
        tier_sizes.append(current_size)
        num_players -= current_size
        tiers -= 1
        current_size = math.floor(num_players / tiers)
    tier_sizes.append(num_players)
    return tier_sizes


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

tier_ratio = math.ceil((len(players_clean) + 1) / (len(teams_clean) / len(ROUND_TIMING)))
base_team_list = teams_clean.copy()
available_team_list = []
mini_available_team_list = []
if TIERS:
    for team in base_team_list:
        available_team_list.append([team, 1])
else:
    for team in base_team_list:
        available_team_list.append([team, tier_ratio])

if TIERS:
    tier_data = get_tier_sizes(len(players_clean), len(teams_clean), len(ROUND_TIMING))
else:
    tier_data = [len(players_clean)]
print(tier_data)
draft.run_draft(START_TIME, tier_data, base_path, tier_ratio, ROUND_TIMING, RANDOM_ORDER, OUTPUT_MODE, players_clean,
                available_team_list, random_teams, teams_clean, event_name)
