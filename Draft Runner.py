import random
import os
import json
import pandas as pd
import math

# SETTINGS

ROUND_TIMING = [2, 2, 2]
START_TIME = [8, 0]
SAVE_DIR = r"E:\_Python Projects\Draft Runner Data"
OUTPUT_MODE = "CD"
RANDOM_ORDER = True


# TODO Add a rookie random function
# TODO Tier support

def available_teams(available_teams, tier_ratio):
    # TODO Support better team sorting.

    teams = []
    for team in available_teams:
        if team[1] != 0:
            if tier_ratio > 1:
                teams.append("{} ({})".format(team[0], team[1]))
            else:
                teams.append(team[0])
    teams.sort()
    team_headers = ["Player", "Team 1", "Team 2", "Team 3", "*Status*"]
    i = 0
    team_lists = [["", "", "", "", ""], ["**Available Teams**", "", "", "", ""]]
    mini_team_list = []
    for team in teams:
        if i == 4:
            mini_team_list.append(team)
            team_lists.append(mini_team_list)
            mini_team_list = []
            i = 0
        else:
            mini_team_list.append(team)
            i += 1
    if len(mini_team_list) > 0:
        for number in range(len(mini_team_list), 5):
            mini_team_list.append("-")

        team_lists.append(mini_team_list)
    # print(team_lists)
    return pd.DataFrame(team_lists, columns=team_headers)


def time_math(hour, minute, additions, margin):
    if margin == 0:
        pass
    else:
        for j in range(0, additions):
            minute += margin
            if minute >= 60:
                hour += 1
                minute -= 60
        if minute < 10:
            string_minute = "0" + str(minute)
        else:
            string_minute = minute
    return (str(hour) + ":" + str(string_minute)), hour, minute


def setup_draft(start_hour, start_minute, players):
    number_of_teams = len(players)
    r2_stats = time_math(start_hour, start_minute, number_of_teams - 1, ROUND_TIMING[0])
    r3_stats = time_math(r2_stats[1], r2_stats[2], number_of_teams + 1, ROUND_TIMING[1])
    table = []

    i = 0
    for player in players:
        team_setup = [player, time_math(start_hour, start_minute, i, ROUND_TIMING[0])[0],
                      time_math(r2_stats[1], r2_stats[2], (number_of_teams - i), ROUND_TIMING[1])[0],
                      time_math(r3_stats[1], r3_stats[2], i, ROUND_TIMING[2])[0], "*Live Picking*"]
        table.append(team_setup)
        i += 1
    return table


def current_slot(df, number_of_players):
    index = ["Team 1", "Team 2", "Team 3"]

    for player in range(0, number_of_players):
        if ":" in df.at[player, index[0]]:
            return [player, index[0]]
    for player in range(number_of_players - 1, -1, -1):
        if ":" in df.at[player, index[1]]:
            return [player, index[1]]
    for player in range(0, number_of_players):
        if ":" in df.at[player, index[2]]:
            return [player, index[2]]
    return None


def swap_index(df, number_of_players, team):
    index = ["Team 1", "Team 2", "Team 3"]
    results = []
    for player in range(0, number_of_players):
        if df.at[player, index[0]] == team:
            results.append([player, index[0]])
    for player in range(number_of_players - 1, -1, -1):
        if df.at[player, index[1]] == team:
            results.append([player, index[1]])
    for player in range(0, number_of_players):
        if df.at[player, index[2]] == team:
            results.append([player, index[2]])
    if not results:
        return None
    return results


def get_team_info(team, available_team_list, mode):
    trying = True
    failed = None
    while trying:
        if team in teams_clean:
            for current_team in available_team_list:
                if team in current_team and trying is True:
                    return current_team
                else:
                    if failed is None:
                        failed = True
        trying = False
    if failed:
        return None


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
    if RANDOM_ORDER:  # If random order setting is activated.
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
draft_info = setup_draft(START_TIME[0], START_TIME[1], players_clean)
headers = ["Player", "Team 1", "Team 2", "Team 3", "*Status*"]
draft_output = pd.DataFrame(draft_info, columns=headers)

# Setting required variables

number_of_players = len(players_clean)

# Checked for Saved Lists
for player in players_clean:
    player_list_location = "{}\{}.txt".format(base_path, player)
    if os.path.isfile(player_list_location):
        for index in range(0, number_of_players):
            stuff = draft_output.at[index, "Player"]
            if player == draft_output.at[index, "Player"]:
                draft_output.at[index, "*Status*"] = "*List*"

teams_output = available_teams(available_team_list, tier_ratio)
total_output = draft_output.append(teams_output, ignore_index=True)

if OUTPUT_MODE == "CD":
    total_output.to_clipboard(excel=True, index=False)
    print(draft_output)

slot_index = current_slot(total_output, number_of_players)

while True:
    # Recieve input
    command = input("Enter your command: ")
    commands = command.split(" ")
    failed = False
    if slot_index is None:
        print("Done Draft")
    else:  # Not complete draft

        # ======================================PICK CODE======================================

        if commands[0].lower() == "pick" or commands[0].lower() == "p":
            if len(commands) != 2:
                print("Please check your formatting")
            else:
                trying = True
                failed = None
                while trying:
                    for current_team in available_team_list:
                        if commands[1] in current_team and trying is True:
                            if current_team[1] != 0:
                                available_team_list.remove(current_team)
                                available_team_list.append([current_team[0], (current_team[1] - 1)])
                                draft_output.at[slot_index[0], slot_index[1]] = commands[1]
                                draft_output.at[slot_index[0], "*Status*"] = "*Live Picking*"
                                trying = False
                                failed = False
                        else:
                            if failed is None:
                                failed = True
                    trying = False
                if failed:
                    print("Invalid Pick")
    # ======================================SWAP CODE======================================

    if commands[0].lower() == "swap" or commands[0].lower() == "s":

        if len(commands) != 3:  # Check to make sure all commands exist
            print("Incorrect formatting! Please format like: swap [swap out team] [swapped in team]")
        else:
            swap_index1 = swap_index(draft_output, number_of_players, commands[1])
            if swap_index1 is not None:  # Did it find team at commands 2?
                if len(swap_index1) > 1:
                    print("================= Choose the correct slot to swap.. =================")
                    drafter_name_index = {}
                    drafter_slot_index = {}
                    for slot in swap_index1:
                        drafter_name = draft_output.at[slot[0], "Player"]
                        drafter_name_index.update({drafter_name: slot[0]})
                        drafter_slot_index.update({drafter_name: slot[1]})
                        print("{} for {}".format(drafter_name, slot[1]))
                    successful = False
                    while successful is False:
                        input_name = input("Enter the player to recieve the swap: ")
                        try:
                            swap_index1 = [drafter_name_index[input_name], drafter_slot_index[input_name]]
                            successful = True
                        except:
                            print("Please check your player input.")
                else:
                    swap_index1 = swap_index1[0]
                team1 = get_team_info(commands[1], available_team_list, "drop")
                team2 = get_team_info(commands[2], available_team_list, "add")
                if team1 is not None:
                    if team2 is not None:
                        # Decrease
                        if team2[1] != 0:
                            available_team_list.remove(team2)
                            available_team_list.append([team2[0], team2[1] - 1])
                        else:
                            failed = True
                        if failed is False:
                            # Increase
                            available_team_list.remove(team1)
                            available_team_list.append([team1[0], team1[1] + 1])
                        draft_output.at[swap_index1[0], swap_index1[1]] = commands[2]
                        draft_output.at[swap_index1[0], "*Status*"] = "*Live Picking*"
                    else:
                        print("{} not available".format(commands[2]))
                        failed = True
                else:
                    print("{} not available".format(commands[1]))
                    failed = True
            else:
                print("Doesn't work like this")
                # swap_index2 = swap_index(draft_output, number_of_players, commands[2])
                # if len(swap_index2) > 1:
                #     print("================= Choose the correct slot to swap.. =================")
                #     drafter_name_index = {}
                #     drafter_slot_index = {}
                #     for slot in swap_index2:
                #         drafter_name = draft_output.at[slot[0], "Player"]
                #         drafter_name_index.update({drafter_name: slot[0]})
                #         drafter_slot_index.update({drafter_name: slot[1]})
                #         print("{} for {}".format(drafter_name, slot[1]))
                #     successful = False
                #     while successful is False:
                #         input_name = input("Enter the player to recieve the swap: ")
                #         try:
                #             swap_index2 = [drafter_name_index[input_name], drafter_slot_index[input_name]]
                #             successful = True
                #         except:
                #             print("Please check your player input.")
                #
                # team1 = get_team_info(commands[1], available_team_list)
                # team2 = get_team_info(commands[2], available_team_list)
                # if team1 is not None:
                #     if team2 is not None:
                #         # Decrease
                #         if team1[1] != 0:
                #             available_team_list.remove(team1)
                #             available_team_list.append([team1[0], team1[1] - 1])
                #         else:
                #             failed = True
                #         if team2[1] != 0 and failed is False:
                #             # Increase
                #             available_team_list.remove(team2)
                #             available_team_list.append([team2[0], team2[1] + 1])
                #         draft_output.at[swap_index2[0], swap_index2[1]] = commands[2]
                #         draft_output.at[slot_index[0], "*Status*"] = "*Live Picking*"
                #     else:
                #         print("{} not available".format(commands[2]))
                #         failed = True
                # else:
                #     print("{} not available".format(commands[1]))
                #     failed = True
    # ======================================RANDOM CODE======================================

    if commands[0].lower() == "random" or commands[0].lower() == "r":
        trying = True
        for random_team in random_teams:
            for available_team in available_team_list:
                if available_team[0] == random_team and trying is True and available_team[1] != 0:
                    draft_output.at[slot_index[0], slot_index[1]] = random_team
                    available_team_list.remove(available_team)
                    available_team_list.append([available_team[0], available_team[1] - 1])
                    if draft_output.at[slot_index[0], "*Status*"] == "*Live Picking*" or draft_output.at[
                        slot_index[0], "*Status*"] == "*List*":
                        if slot_index[1] == "Team 1":
                            draft_output.at[slot_index[0], "*Status*"] = "*MIA*"
                        else:
                            draft_output.at[slot_index[0], "*Status*"] = "*Missing*"
                    trying = False

    # ======================================LIST SETUP CODE======================================

    if commands[0].lower() == "list" or commands[0].lower() == "l":
        if len(commands) != 2:
            print("Incorrect formatting, please use list [player name]")
            failed = True
        else:
            if commands[1] in players_clean:
                player_list_location = "{}\{}.txt".format(base_path, commands[1])

                if os.path.isfile(player_list_location):
                    print("True")
                    pass
                else:
                    f = open(player_list_location, "w")
                    f.close()
                df = os.system("notepad.exe {}".format(player_list_location))
                draft_output.at[players_clean.index(commands[1]), "*Status*"] = "*List*"
            else:
                print("Invalid player, ensure capitalization is the same.")
                failed = True

    if commands[0].lower() == "exit" or commands[0].lower() == "end" or commands[0].lower() == "quit":
        break

    if commands[0].lower() == "print":
        print(total_output)

    if failed is False:
        list_active = True
        while list_active:
            # Output Results
            teams_output = available_teams(available_team_list, tier_ratio)
            total_output = draft_output.append(teams_output, ignore_index=True)

            if OUTPUT_MODE == "CD":
                total_output.to_clipboard(excel=True, index=False)

            slot_index = current_slot(total_output, number_of_players)
            if slot_index is not None:
                if draft_output.at[slot_index[0], "*Status*"] == "*List*":
                    print("Yo they got a list for {}!".format(draft_output.at[slot_index[0], "Player"]))
                    player_list_location = "{}\{}.txt".format(base_path, draft_output.at[slot_index[0], "Player"])
                    f = open(player_list_location, "r")
                    player_list_teams = f.readlines()
                    player_list_teams_clean = [x.replace('\n', '') for x in player_list_teams]
                    trying = True
                    found_team = False
                    for player_team in player_list_teams_clean:
                        for available_team in available_team_list:
                            if available_team[0] == player_team and trying is True and available_team[1] != 0:
                                draft_output.at[slot_index[0], slot_index[1]] = player_team
                                available_team_list.remove(available_team)
                                available_team_list.append([available_team[0], available_team[1] - 1])
                                trying = False
                                found_team = True

                    if found_team is False:
                        print("No valid picks on list, finding next random team.")
                        trying = True
                        for random_team in random_teams:
                            for available_team in available_team_list:
                                if available_team[0] == random_team and trying is True and available_team[1] != 0:
                                    draft_output.at[slot_index[0], slot_index[1]] = random_team
                                    available_team_list.remove(available_team)
                                    available_team_list.append([available_team[0], available_team[1] - 1])
                                    trying = False
                elif draft_output.at[slot_index[0], "*Status*"] == "*MIA*" or draft_output.at[
                    slot_index[0], "*Status*"] == "*Missing*":
                    trying = True
                    for random_team in random_teams:
                        for available_team in available_team_list:
                            if available_team[0] == random_team and trying is True and available_team[1] != 0:
                                draft_output.at[slot_index[0], slot_index[1]] = random_team
                                available_team_list.remove(available_team)
                                available_team_list.append([available_team[0], available_team[1] - 1])
                                trying = False

                else:
                    list_active = False
            else:
                list_active = False
            print("@{} is up now".format(draft_output.at[slot_index[0], "Player"]))
