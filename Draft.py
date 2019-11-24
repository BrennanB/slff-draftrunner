import os
import pandas as pd
import re
import gspread
import gspread_dataframe
from oauth2client.service_account import ServiceAccountCredentials



def available_teams(available_team_list, tier_ratio):
    displayed_teams = []
    for team in available_team_list:
        if team[1] != 0:
            displayed_teams.append(team)

    if tier_ratio > 1:  # Multiple teams are required
        teams = ["{} ({})".format(team[0], team[1]) for team in displayed_teams]
    else:  # Single teams only
        teams = [team[0] for team in displayed_teams]

    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    teams.sort(key=alphanum_key)
    team_headers = ["Player", "Team 1", "Team 2", "Team 3", "*Status*", "--", "Random List"]
    i = 0
    team_lists = [["", "", "", "", "", "", ""], ["**Available Teams**", "", "", "", "", "", ""]]
    mini_team_list = []
    for team in teams:
        if i == 6:
            mini_team_list.append(team)
            team_lists.append(mini_team_list)
            mini_team_list = []
            i = 0
        else:
            mini_team_list.append(team)
            i += 1
    if len(mini_team_list) > 0:
        for number in range(len(mini_team_list), 7):
            mini_team_list.append("-")

        team_lists.append(mini_team_list)
    # print(team_lists)
    return pd.DataFrame(team_lists, columns=team_headers), available_team_list


def time_math(hour, minute, additions, margin):
    if margin == 0:
        return None
    else:
        for i in range(0, additions):
            minute += margin
            if minute >= 60:
                hour += 1
                minute -= 60
        if minute < 10:
            string_minute = "0" + str(minute)
        else:
            string_minute = minute
    return "{}:{}".format(hour, string_minute), hour, minute


def setup_draft(start_hour, start_minute, players, ROUND_TIMING):
    number_of_teams = len(players)
    r2_stats = time_math(start_hour, start_minute, number_of_teams - 1, ROUND_TIMING[0])
    r3_stats = time_math(r2_stats[1], r2_stats[2], number_of_teams + 1, ROUND_TIMING[1])
    table = []
    i = 0
    for player in players:
        team_setup = [player, time_math(start_hour, start_minute, i, ROUND_TIMING[0])[0],
                      time_math(r2_stats[1], r2_stats[2], (number_of_teams - i), ROUND_TIMING[1])[0],
                      time_math(r3_stats[1], r3_stats[2], i, ROUND_TIMING[2])[0], "*Live Picking*", "", ""]
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


def get_team_info(team, available_team_list, mode, teams_clean):
    for current_team in available_team_list:
        if team in teams_clean:
            if team in current_team:
                return current_team
    else:
        return None


def randoms_visual_update(df, random_teams, number_of_players, available_team_list):

    for i in range(0, number_of_players):
        trying = True
        i2 = 0
        for random_team in random_teams:
            for available_team in available_team_list:
                if available_team[0] == random_team and trying is True and available_team[1] != 0:
                    if i == 0:
                        df.at[i, "Random List"] = "*({})*".format(random_team)
                        trying = False
                    else:
                        df.at[i, "Random List"] = "*-*"
                    i2 += 1
                    if i2 == (i+1):
                        df.at[i, "Random List"] = "*({})*".format(random_team)
                        trying = False
                    else:
                        df.at[i, "Random List"] = "*-*"
    return df


def check_saved_lists(base_path, players_clean, number_of_players, draft_output):
    # Checked for Saved Lists
    for player in players_clean:
        player_list_location = "{}\{}.txt".format(base_path, player)
        if os.path.isfile(player_list_location):
            for index in range(0, number_of_players):
                if player == draft_output.at[index, "Player"]:
                    draft_output.at[index, "*Status*"] = "*List*"
    return draft_output


def determine_swap_player(swap_index, draft_output):
    print("================= Choose the correct slot to swap.. =================")
    drafter_name_index = {}
    drafter_slot_index = {}
    for slot in swap_index:
        drafter_name = draft_output.at[slot[0], "Player"]
        drafter_name_index.update({drafter_name: slot[0]})
        drafter_slot_index.update({drafter_name: slot[1]})
        print("{} for {}".format(drafter_name, slot[1]))
    successful = False
    while successful is False:
        input_name = input("Enter the player to recieve the swap: ")
        try:
            return [drafter_name_index[input_name], drafter_slot_index[input_name]]
        except:
            print("Please check your player input.")


def check_and_run_lists(tier_data, tier_ratio, available_team_list, draft_output, number_of_players, base_path, random_teams):

    list_active = True
    while list_active:
        # Output Results
        if len(tier_data) == 1:
            teams_output = available_teams(available_team_list, tier_ratio)
        else:
            teams_output = available_teams(available_team_list, 1)
        available_team_list = teams_output[1]
        total_output = draft_output.append(teams_output[0], ignore_index=True)

        slot_index = current_slot(total_output, number_of_players)
        if slot_index is not None:
            if draft_output.at[slot_index[0], "*Status*"] == "*List*":
                print("Yo they got a list for {}!".format(draft_output.at[slot_index[0], "Player"]))
                player_list_location = "{}\{}.txt".format(base_path,
                                                          draft_output.at[slot_index[0], "Player"])
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
                            if available_team[0] == random_team and trying is True and \
                                    available_team[1] != 0:
                                draft_output.at[slot_index[0], slot_index[1]] = random_team
                                available_team_list.remove(available_team)
                                available_team_list.append([available_team[0], available_team[1] - 1])
                                trying = False
            elif draft_output.at[slot_index[0], "*Status*"] == "*MIA*" or \
                    draft_output.at[slot_index[0], "*Status*"] == "*Missing*":
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
    return {"slot_index": slot_index, "available_team_list": available_team_list, "draft_output": draft_output}


def create_draft(players_clean, tier_data, START_TIME, ROUND_TIMING, base_path, available_team_list, tier_ratio,
                 OUTPUT_MODE, random_teams, event_name):

    # DRAFT CREATION SECTION
    number_of_players = len(players_clean)
    d = {}
    tiered_available_team_list = {}

    if len(tier_data) > 1:
        tiered_players_clean = list()
        i = 0
        tier_index = 1
        for tier in tier_data:  # Create each iteration of tiered draft.
            past_i = i
            i += (tier + 1)
            if past_i != 0:
                tiered_players_clean.append(players_clean[(past_i - (tier_index - 1)):(i - tier_index)])
                draft_info = setup_draft(START_TIME[0], START_TIME[1],
                                         players_clean[(past_i - (tier_index - 1)):(i - tier_index)], ROUND_TIMING)
            else:
                tiered_players_clean.append(players_clean[(past_i):(i - 1)])
                draft_info = setup_draft(START_TIME[0], START_TIME[1], players_clean[(past_i):(i - 1)],
                                         ROUND_TIMING)
            headers = ["Player", "Team 1", "Team 2", "Team 3", "*Status*", "--", "Random List"]
            d[tier_index] = pd.DataFrame(draft_info, columns=headers)
            # Checked for Saved Lists
            if past_i != 0:
                for player in players_clean[(past_i - (tier_index - 1)):(i - tier_index)]:
                    player_list_location = "{}\{}.txt".format(base_path, player)
                    if os.path.isfile(player_list_location):
                        for index in range(0, len(players_clean[(past_i - (tier_index - 1)):(i - tier_index)])):
                            draft_output = d[tier_index]
                            if player == draft_output.at[index, "Player"]:
                                draft_output.at[index, "*Status*"] = "*List*"
                                list_results = check_and_run_lists(tier_data, tier_ratio, available_team_list,
                                                                   draft_output,
                                                                   number_of_players, base_path, random_teams)
                                available_team_list = list_results['available_team_list']
                                draft_output = list_results['draft_output']
                                d.update({tier_index: draft_output})
            else:
                for player in players_clean[(past_i):(i - 1)]:
                    player_list_location = "{}\{}.txt".format(base_path, player)
                    if os.path.isfile(player_list_location):
                        for index in range(0, len(tiered_players_clean[tier_index - 1])):
                            draft_output = d[tier_index]
                            if player == draft_output.at[index, "Player"]:
                                draft_output.at[index, "*Status*"] = "*List*"
                                d.update({tier_index: draft_output})
            tiered_available_team_list.update({tier_index: available_team_list[:]})
            tier_index += 1
        print("There are {} tiers, to post the tiers, please use the 'print' command".format(len(tier_data)))
        return {"tiered_available_team_list": tiered_available_team_list, "d": d, "tiered_players_clean": tiered_players_clean}
    else:  # Tiers aren't being run
        draft_info = setup_draft(START_TIME[0], START_TIME[1], players_clean, ROUND_TIMING)
        headers = ["Player", "Team 1", "Team 2", "Team 3", "*Status*", "--", "Random List"]
        draft_output = pd.DataFrame(draft_info, columns=headers)
        tiered_players_clean = None

        draft_output = check_saved_lists(base_path, players_clean, number_of_players, draft_output)
        list_results = check_and_run_lists(tier_data, tier_ratio, available_team_list, draft_output,
                                           number_of_players, base_path, random_teams)
        slot_index = list_results['slot_index']
        available_team_list = list_results['available_team_list']
        draft_output = list_results['draft_output']
        teams_output = available_teams(available_team_list, tier_ratio)
        available_team_list = teams_output[1]
        total_output = draft_output.append(teams_output[0], ignore_index=True)


        if OUTPUT_MODE == "CD":
            total_output = randoms_visual_update(total_output, random_teams, number_of_players, available_team_list)

            if slot_index is not None:
                player_up = "@{}".format(draft_output.at[slot_index[0], "Player"])
            else:
                player_up = "Done!"
            headers = ["Player", "Team 1", "Team 2", "Team 3", "*Status*", "--", "Random List"]
            ping_data = [["-", "", "", "", "", "", ""],
                         [player_up, "is up", "", "", "", "", event_name]]
            player_ping = pd.DataFrame(ping_data, columns=headers)
            super_output = total_output.append(player_ping, ignore_index=True)
            super_output.to_clipboard(excel=True, index=False)
            print(super_output)
        return {"slot_index": slot_index, "draft_output": draft_output, "number_of_players": number_of_players}


def run_draft(START_TIME, tier_data, base_path, tier_ratio, ROUND_TIMING, RANDOM_ORDER, OUTPUT_MODE, players_clean,
              available_team_list, random_teams, teams_clean, event_name):

    draft_info = create_draft(players_clean, tier_data, START_TIME, ROUND_TIMING, base_path, available_team_list,
                              tier_ratio, OUTPUT_MODE, random_teams, event_name)

    if len(tier_data) > 1:
        d = draft_info['d']
        tiered_players_clean = draft_info['tiered_players_clean']
        tiered_available_team_list = draft_info['tiered_available_team_list']
    else:
        slot_index = draft_info['slot_index']
        draft_output = draft_info['draft_output']
        number_of_players = draft_info['number_of_players']

    # COMMANDS SECTION
    #TODO Lists don't auto-complete when the first player has a list, and the data has been loaded
    while True:
        # Receive input
        commands = input("Enter your command: ").split(" ")
        valid_command, printed = False, False

        if len(tier_data) > 1:
            tier_value = commands[0]
            if tier_value[:1].lower() == 't':
                if len(tier_value[1:]) > 0:
                    try:
                        if int(tier_value[1:]) <= tier_ratio:
                            valid_command = True
                            draft_output = d[int(tier_value[1:])]
                            number_of_players = (tier_data[int(tier_value[1:])-1])
                            slot_index = current_slot(draft_output, number_of_players)
                            players_clean = tiered_players_clean[int(tier_value[1:])-1]
                            available_team_list = tiered_available_team_list[int(tier_value[1:])]
                            commands.pop(0)
                    except ValueError:
                        print("'{}' is not a number, please use a number for the tier value".format(tier_value[1:]))
                else:
                    print("Please enter a tier number.")
            else:
                print("Please specify a tier as 't(tier number)' for example t2 for tier 2")
        else:
            valid_command = True
            tier_value = None

        super_failed = False
        if valid_command and len(commands) != 0:  # If tier value exists, or if there are no tiers.
            # ======================================PICK CODE======================================
            if commands[0].lower() == "pick" or commands[0].lower() == "p":
                if slot_index is None:
                    print("Draft is complete, this command is not available.")
                else:  # Not complete draft
                    if len(commands) != 2:
                        print("Please check your formatting")
                    else:
                        for current_team in available_team_list:
                            if commands[1] in current_team:
                                if current_team[1] != 0:
                                    available_team_list.remove(current_team)
                                    available_team_list.append([current_team[0], (current_team[1] - 1)])
                                    draft_output.at[slot_index[0], slot_index[1]] = commands[1]
                                    draft_output.at[slot_index[0], "*Status*"] = "*Live Picking*"
                                    break
                        else:
                            super_failed = True
                            print("Invalid Pick")
            # ======================================SWAP CODE======================================

            elif commands[0].lower() == "swap" or commands[0].lower() == "s":

                if len(commands) != 3:  # Check to make sure all commands exist
                    print("Incorrect formatting! Please format like: swap [swap out team] [swapped in team]")
                else:
                    swap_index1 = swap_index(draft_output, number_of_players, commands[1])
                    swap_index2 = swap_index(draft_output, number_of_players, commands[2])
                    if swap_index1 is not None:  # Did it find team at commands 2?
                        print(available_team_list)
                        raw_team_numbers = []
                        for team in available_team_list:
                            if team[1] != 0:
                                raw_team_numbers.append(team[0])
                        print(swap_index2 not in raw_team_numbers)
                        print(raw_team_numbers)
                        if swap_index2 is not None and commands[2] not in raw_team_numbers:

                            '''Both teams are picked'''
                            #TODO Add player team swap compatibility for multiple team drafts

                            if len(swap_index1) > 1:
                                swap_index1 = determine_swap_player(swap_index1, draft_output)
                            else:
                                swap_index1 = swap_index1[0]
                            if len(swap_index2) > 1:
                                swap_index2 = determine_swap_player(swap_index2, draft_output)
                            else:
                                swap_index2 = swap_index2[0]

                            if len(swap_index1) == 1 and len(swap_index2) == 1:
                                draft_output.at[swap_index1[0][0], swap_index1[0][1]] = commands[2]
                                draft_output.at[swap_index1[0][0], "*Status*"] = "*Live Picking*"
                                draft_output.at[swap_index2[0][0], swap_index2[0][1]] = commands[1]
                                draft_output.at[swap_index2[0][0], "*Status*"] = "*Live Picking*"
                            else:
                                print(swap_index1)
                                print(swap_index2)
                                draft_output.at[swap_index1[0], swap_index1[1]] = commands[2]
                                draft_output.at[swap_index1[0], "*Status*"] = "*Live Picking*"
                                draft_output.at[swap_index2[0], swap_index2[1]] = commands[1]
                                draft_output.at[swap_index2[0], "*Status*"] = "*Live Picking*"
                        else:
                            if len(swap_index1) > 1:
                                swap_index1 = determine_swap_player(swap_index1, draft_output)
                            else:
                                swap_index1 = swap_index1[0]
                            team1 = get_team_info(commands[1], available_team_list, "drop", teams_clean)
                            team2 = get_team_info(commands[2], available_team_list, "add", teams_clean)
                            failed = False
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
                                    super_failed = True
                            else:
                                print("{} not available".format(commands[1]))
                                super_failed = True
                    else:
                        super_failed = True
                        print("Doesn't work like this")
            # ======================================RANDOM CODE======================================

            elif commands[0].lower() == "random" or commands[0].lower() == "r":
                if slot_index is None:
                    print("Draft is complete, this command is not available.")
                else:  # Not complete draft
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
            elif commands[0].lower() == "list" or commands[0].lower() == "l":
                if len(commands) != 2:
                    print("Incorrect formatting, please use list [player name]. Player names are caps sensitive.")
                    super_failed = True
                else:
                    if commands[1] in players_clean:
                        player_list_location = "{}\{}.txt".format(base_path, commands[1])

                        if os.path.isfile(player_list_location):
                            pass
                        else:
                            f = open(player_list_location, "w")
                            f.close()
                        df = os.system("notepad.exe {}".format(player_list_location))
                        print(commands)
                        print(players_clean)
                        print(players_clean.index(commands[1]))
                        draft_output.at[players_clean.index(commands[1]), "*Status*"] = "*List*"
                    else:
                        print("Invalid player, ensure capitalization is the same.")
                        super_failed = True

            elif commands[0].lower() == "exit" or commands[0].lower() == "end" or commands[0].lower() == "quit":
                break

            elif commands[0].lower() == "print":
                if OUTPUT_MODE == "CD":
                    if len(tier_data) == 1:
                        teams_output = available_teams(available_team_list, tier_ratio)
                    else:
                        teams_output = available_teams(available_team_list, 1)
                    available_team_list = teams_output[1]
                    total_output = draft_output.append(teams_output[0], ignore_index=True)
                    printed = True
                    total_output = randoms_visual_update(total_output, random_teams, number_of_players,
                                                         available_team_list)
                    if slot_index is not None:
                        player_up = "@{}".format(draft_output.at[slot_index[0], "Player"])
                    else:
                        player_up = "Done!"
                    headers = ["Player", "Team 1", "Team 2", "Team 3", "*Status*", "--", "Random List"]
                    if len(tier_data) > 1:
                        if player_up != "Done!":
                            ping_data = [["-", "", "", "", "", "", ""],
                                         [player_up, "is up", "", "", "", "",
                                          "T{} at {}".format(tier_value[1:], event_name)]]
                        else:
                            ping_data = [["-", "", "", "", "", "", ""],
                                         [player_up, "", "", "", "", "",
                                          "T{} at {}".format(tier_value[1:], event_name)]]
                    else:
                        if player_up != "Done!":
                            ping_data = [["-", "", "", "", "", "", ""],
                                     [player_up, "is up", "", "", "", "", event_name]]
                        else:
                            ping_data = [["-", "", "", "", "", "", ""],
                                         [player_up, "", "", "", "", "", event_name]]
                    player_ping = pd.DataFrame(ping_data, columns=headers)
                    super_output = total_output.append(player_ping, ignore_index=True)
                    super_output.to_clipboard(excel=True, index=False)
                    print(super_output)

            elif commands[0].lower() == "delay":
                # Delay draft by x minutes
                if len(commands) != 2 or int(commands[1]) > 60:
                    print("Please use the command with a delay in minutes, make sure you don't delay more than 60minutes.")
                    super_failed = True
                else:
                    local_num_players = len(draft_output.index)
                    for index in range(0, local_num_players):
                        for column in ["Team 1", "Team 2", "Team 3"]:
                            try:
                                current_time = draft_output.at[index, column]
                                current_time = [int(x) for x in current_time.split(":")]
                                new_base_time = time_math(current_time[0], current_time[1], 1, int(commands[1]))
                                draft_output.at[index, column] = new_base_time[0]
                            except:
                                pass
            elif commands[0].lower() == "remaining":
                remaining_teams = ""
                for team_data in available_team_list:
                    for i in range(0, team_data[1]):
                        remaining_teams += "{}\n".format(team_data[0])

                print(remaining_teams)
                super_failed = True

            else:
                super_failed = True
                print("{} is not a valid command".format(commands[0]))

            if super_failed is False:
                list_results = check_and_run_lists(tier_data, tier_ratio, available_team_list, draft_output,
                                                   number_of_players, base_path, random_teams)
                slot_index = list_results['slot_index']
                available_team_list = list_results['available_team_list']
                draft_output = list_results['draft_output']
                if OUTPUT_MODE == "CD" and printed is False:
                    if len(tier_data) == 1:
                        teams_output = available_teams(available_team_list, tier_ratio)
                    else:
                        teams_output = available_teams(available_team_list, 1)
                    available_team_list = teams_output[1]
                    total_output = draft_output.append(teams_output[0], ignore_index=True)
                    total_output = randoms_visual_update(total_output, random_teams, number_of_players,
                                                         available_team_list)
                    if slot_index is not None:
                        player_up = "@{}".format(draft_output.at[slot_index[0], "Player"])
                    else:
                        player_up = "Done!"
                    headers = ["Player", "Team 1", "Team 2", "Team 3", "*Status*", "--", "Random List"]
                    if len(tier_data) > 1:
                        if player_up != "Done!":
                            ping_data = [["-", "", "", "", "", "", ""],
                                         [player_up, "is up", "", "", "", "",
                                          "T{} at {}".format(tier_value[1:], event_name)]]
                        else:
                            ping_data = [["-", "", "", "", "", "", ""],
                                         [player_up, "", "", "", "", "",
                                          "T{} at {}".format(tier_value[1:], event_name.lower())]]
                    else:
                        if player_up != "Done!":
                            ping_data = [["-", "", "", "", "", "", ""],
                                     [player_up, "is up", "", "", "", "", event_name.lower()]]
                        else:
                            ping_data = [["-", "", "", "", "", "", ""],
                                         [player_up, "", "", "", "", "", event_name.lower()]]
                    player_ping = pd.DataFrame(ping_data, columns=headers)
                    super_output = total_output.append(player_ping, ignore_index=True)
                    super_output.to_clipboard(excel=True, index=False)
                    print(super_output)
                    if len(tier_data) > 1:
                        d.update({int(tier_value[1:]): draft_output})
                        tiered_available_team_list.update({int(tier_value[1:]): available_team_list})

            # Logging onto spreadsheet


            draft_log = draft_output.copy()
            draft_log = draft_log.drop(columns=['--', 'Random List'])
            keys = []
            identifier = []
            for i in range(0, draft_log.shape[0]):
                keys.append(event_name.lower())
                identifier.append("{}_{}".format(draft_log.at[i, 'Player'], event_name.lower()))
            draft_log['Event'] = keys
            draft_log.insert(0, "Identifier", identifier, True)

            try:
                scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                credentials = ServiceAccountCredentials.from_json_keyfile_name('SLFF Draft Runner-e9d03ff02c79.json', scope)
                gc = gspread.authorize(credentials)
                stuff = gc.open('SLFF 2019-2020 Main Spreadsheet')
                wks = stuff.worksheet('Results')

                old_logs = gspread_dataframe.get_as_dataframe(wks)
                old_logs = old_logs[~old_logs.Event.str.contains(event_name.lower())]
                old_logs = old_logs.append(draft_log, ignore_index=True)
                gspread_dataframe.set_with_dataframe(wks, old_logs)
            except Exception as e:
                print("Failed to upload to google sheets. You may have an incorrectly set up API key, or no internet access currently")
                print(e)

        else:
            print("Invalid Command, please enter more than just tier value")