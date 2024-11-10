import re

import utils.db as db

from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime
import random

lastUserListRefresh = datetime.now()
lastTriggerListRefresh = datetime.now()
firstRefresh = True
tileRaceUserList = []
triggerList = []

THREAD_ID = os.environ.get("THREAD_ID", "")
#
# KC_REGEX = "your [\w\W]+ count is: ([0-9]+)\."
# COIN_TO_STAR_THRESHOLD = 10
# MAX_SIDE_QUEST_COINS = 8
#
# def is_user_in_race(rsn):
#     # lower case name first
#     userId = db.get_user_from_username(rsn.lower())
#     if userId is None:
#         return False
#
#     return not db.get_team(userId) is None
#
# def parse_kc_type(item: str) -> str:
#     if "tombs of amascut" in item:
#         if "tombs of amascut: entry mode" in item:
#             return "tombs of amascut entry mode"
#         elif "tombs of amascut: expert mode" in item:
#             return "tombs of amascut expert mode"
#         return "tombs of amascut"
#     elif "chambers of xeric" in item:
#         if  "chambers of xeric challenge mode" in item:
#             return "chambers of xeric challenge mode"
#         return "chambers of xeric"
#     elif "theatre of blood" in item:
#         if "theatre of blood: entry mode" in item:
#             return "theatre of blood entry mode"
#         elif "theatre of blood: hard mode" in item:
#             return "theatre of blood hard mode"
#         return "theatre of blood"
#     elif "giant mole" in item:
#         return "giant mole"
#     elif "scurrius" in item:
#         return "scurrius"
#     elif "tzkal-zuk" in item:
#         return "tzkal-zuk"
#     elif "tztok-jad" in item:
#         return "tztok-jad"
#     elif "agility pyramid" in item:
#         return "agility pyramid"
#     elif "agility arena" in item:
#         return "agility arena"
#     else:
#         return "Not Implemented"
#
# def add_side_quest_progress(team, tile, item, trigger, progress = 1):
#     completion = False
#     # Check if the count for the trigger is met
#     trigger_count = trigger["count"]
#     # get the current count for the trigger from the database
#     side_progress = db.get_side_progress(team, tile)
#
#     if item in side_progress:
#         side_progress[item]["value"] = int(side_progress[item]["value"]) + progress
#     else:
#         side_progress[item] = {}
#         side_progress[item]["value"] = progress
#     current_count = side_progress[item]["value"]
#
#     if current_count >= trigger_count:
#         side_coins_gained = 0
#         for i in side_progress:
#             if "gained" in side_progress[i]:
#                 side_coins_gained += side_progress[i]["gained"]
#
#         if side_coins_gained >= MAX_SIDE_QUEST_COINS:
#             return False
#
#         trigger_points = trigger["points"]
#         if "gained" in side_progress[item]:
#             trigger_points = min(MAX_SIDE_QUEST_COINS - side_progress[item]["gained"], trigger_points)
#             side_progress[item]["gained"] += trigger_points
#         else:
#             side_progress[item]["gained"] = trigger_points
#
#         coins_count = db.get_coin_count(team) 
#         if coins_count + trigger_points >= COIN_TO_STAR_THRESHOLD:
#             db.set_coins(team, coins_count + trigger_points - COIN_TO_STAR_THRESHOLD)
#             db.add_stars(team, 1)
#         else:
#             db.add_coins(team, trigger_points)
#         
#         side_progress[item]["value"] -= trigger_count
#         completion = True
#
#     db.save_side_progress(team, tile, side_progress)
#     return completion
#
# def add_main_quest_progress(team, tile, item, trigger, progress = 1):
#     completion = False
#     # Check if the count for the trigger is met
#     trigger_count = trigger["count"]
#     # get the current count for the trigger from the database
#     main_progress = db.get_main_progress(team, tile)
#
#     if item in main_progress:
#         main_progress[item]["value"] = int(main_progress[item]["value"]) + progress
#     else:
#         main_progress[item] = {}
#         main_progress[item]["value"] = progress
#
#     current_count = 0
#     for t in trigger["trigger"]:
#         # get everything before ":" if there is one
#         t = t.split(":")[0]
#         if t.lower() in main_progress:
#             current_count += main_progress[t.lower()]["value"]
#
#     trigger_count = trigger["count"]
#     if current_count >= trigger_count:
#         db.complete_tile(team, tile)
#         # add stars
#         db.add_stars(team, trigger["points"])
#         completion = True
#     else:
#         db.save_main_progress(team, tile, main_progress)
#
#     return completion

def matches_trigger(trigger_id, trigger, source):
    trigger_data = db.get_trigger(trigger_id)
    # print(trigger_data)
    if trigger_data is None:
        return False

    if len(trigger_data) == 1:
        trigger_data_trigger = trigger_data[0].lower()
        trigger_data_source = ""
    else:
        trigger_data_trigger = trigger_data[0].lower()
        trigger_data_source = trigger_data[1].lower()

    if trigger_data_source == "":
        if trigger_data_trigger == trigger.lower():
            return True
    else:
        if trigger_data_trigger == trigger.lower() and trigger_data_source == source.lower():
            return True

    return False

def get_progress(team, challenge, task):
    progress = db.get_progress(team)
    # print(progress)
    if progress is None:
        db.save_progress(team, {})
        progress = db.get_progress(team)

    return progress[str(challenge)][str(task)] if str(challenge) in progress and str(task) in progress[str(challenge)] else 0

def roll_new_global_challenge():
    globalChallenges = [73, 79, 80, 84, 85, 86, 89, 90, 91]
    currentGlobalChallenge = db.get_global_challenge()
    while currentGlobalChallenge == db.get_global_challenge():
        currentGlobalChallenge = globalChallenges[random.randint(0, len(globalChallenges) - 1)]

    db.set_global_challenge(currentGlobalChallenge)

def get_challenge_triggers(challenge_id):
    triggers = []
    tasks = db.get_challenge_tasks(challenge_id)

    for task in tasks:
        task_triggers = db.get_task_triggers(task)
        triggers.extend(task_triggers)

    # Remove duplicates
    triggers = list(set(triggers))

    return triggers

def complete_challenge(team, challenge_type):
    print(f"Completing {challenge_type} challenge for team {db.get_team_name(team)}")
    tile = db.get_team_tile(team)
    if challenge_type == "Global":
        # If it's a global challenge, complete the global challenge and reset the tile progress
        # Then, create a new global challenge
        progress = db.get_progress(team)
        tile_challenge = db.get_tile_challenge(tile)
        for task in db.get_challenge_tasks(tile_challenge):
            if str(tile_challenge) not in progress:
                progress[str(tile_challenge)] = {}
            progress[str(tile_challenge)][str(task)] = 0

        global_challenge = db.get_global_challenge()
        for task in db.get_challenge_tasks(global_challenge):
            if str(global_challenge) not in progress:
                progress[str(global_challenge)] = {}
            progress[str(global_challenge)][str(task)] = 0

        db.save_progress(team, progress)

        roll_new_global_challenge()

        db.complete_challenge(team, coins = 80, die = 12) # 80 coins and 12 sided die
        db.set_main_die_modifier(team, 0)
        db.set_extra_dice(team, [])
        db.increment_challenge_count()
        db.set_coins_gained_this_tile(team, 0)

        message = f"{db.get_team_name(team)} has completed a {challenge_type} Challenge: {db.get_challenge_name(global_challenge)}\n"
        message += f"They have been awarded 80 coins and a 12 sided die!"
        return message
    elif challenge_type == "Region":
        # If it's a region challenge, complete the region challenge and reset the tile progress
        progress = db.get_progress(team)
        tile_challenge = db.get_tile_challenge(tile)
        for task in db.get_challenge_tasks(tile_challenge):
            if str(tile_challenge) not in progress:
                progress[str(tile_challenge)] = {}
            progress[str(tile_challenge)][str(task)] = 0

        region_challenge = db.get_region_challenge(tile)
        for task in db.get_challenge_tasks(region_challenge):
            if str(region_challenge) not in progress:
                progress[str(region_challenge)] = {}
            progress[str(region_challenge)][str(task)] = 0

        db.save_progress(team, progress)

        db.complete_challenge(team, coins = 40, die = 8) # 20 coins and 8 sided die
        db.set_main_die_modifier(team, 0)
        db.set_extra_dice(team, [])
        db.increment_challenge_count()
        db.set_coins_gained_this_tile(team, 0)

        message = f"{db.get_team_name(team)} has completed a {challenge_type} Challenge: {db.get_challenge_name(region_challenge)}\n"
        message += f"They have been awarded 40 coins and an 8 sided die!"
        return message
    elif challenge_type == "Tile":
        # If it's a tile challenge, complete the tile challenge
        progress = db.get_progress(team)
        tile_challenge = db.get_tile_challenge(tile)
        for task in db.get_challenge_tasks(tile_challenge):
            if str(tile_challenge) not in progress:
                progress[str(tile_challenge)] = {}
            progress[str(tile_challenge)][str(task)] = 0

        db.save_progress(team, progress)

        db.complete_challenge(team, coins = 10, die = 4) # 5 coins and 4 sided die
        db.set_main_die_modifier(team, 0)
        db.set_extra_dice(team, [])
        db.increment_challenge_count()
        db.set_coins_gained_this_tile(team, 0)

        message = f"{db.get_team_name(team)} has completed a {challenge_type} Challenge: {db.get_challenge_name(tile_challenge)}\n"
        message += f"They have been awarded 10 coins and a 4 sided die!"
        return message
    elif challenge_type == "Coin":
        if db.get_coins_gained_this_tile(team) < 10:
            # If it's a coin challenge, complete the coin challenge
            db.add_coins(team, 5)
            db.increment_coins_gained_this_tile(team, 5)

            progress = db.get_progress(team)
            coin_challenge = db.get_coin_challenge(tile)
            for task in db.get_challenge_tasks(coin_challenge):
                if str(coin_challenge) not in progress:
                    progress[str(coin_challenge)] = {}
                progress[str(coin_challenge)][str(task)] = 0

            db.save_progress(team, progress)
            db.increment_challenge_count()

            message = f"{db.get_team_name(team)} has completed a {challenge_type} Challenge: {db.get_challenge_name(coin_challenge)}\n"
            message += f"They have been awarded 5 coins!"
            return message
        else:
            progress = db.get_progress(team)
            coin_challenge = db.get_coin_challenge(tile)
            for task in db.get_challenge_tasks(coin_challenge):
                if str(coin_challenge) not in progress:
                    progress[str(coin_challenge)] = {}
                progress[str(coin_challenge)][str(task)] = 0

            db.save_progress(team, progress)
            db.increment_challenge_count()

            message = f"{db.get_team_name(team)} has completed a {challenge_type} Challenge: {db.get_challenge_name(coin_challenge)}\n"
            message += f"But they have already gained 10 coins this tile, so they have not been awarded any coins!"
            return message


def progress_quest(challenge, team, trigger, source, quantity, challenge_type):
    tasks = db.get_challenge_tasks(challenge)
    for task in tasks:
        # Grab all of the triggers for the task
        triggers = db.get_task_triggers(task)
        for task_trigger in triggers:
            if matches_trigger(task_trigger, trigger, source):
                # Get current progress for the task
                progress = get_progress(team, challenge, task)
                # print(progress)

                updated_progress = progress + quantity
                # print(f"Updated progress: {updated_progress}")

                # Check if the task is complete
                # print(f"task quantity: {db.get_task_quantity(task)}")
                if updated_progress >= db.get_task_quantity(task):
                    # Complete the task
                    message = complete_challenge(team, challenge_type)
                    return {
                        "message": message,
                        "thread_id": THREAD_ID
                    }
                else:
                    db.save_task_progress(team, challenge, task, updated_progress)

    return None

def progress_team(team, trigger, source, quantity = 1, rsn = ""):
    print(f"Progressing {team} ({rsn}) with trigger {trigger} from {source} with quantity {quantity}")
    # Grab the current quests from the team.
    tile = db.get_team_tile(team)
    # print(f"Tile: {tile}")
    
    # Progress the global quest
    # print(f"Global challenge id: {db.get_global_challenge()}")
    progression = progress_quest(db.get_global_challenge(), team, trigger, source, quantity, "Global")
    if progression is not None:
        return progression
    
    # Progress the region quest
    # print(f"Region challenge id: {db.get_region_challenge(tile)}")
    progression = progress_quest(db.get_region_challenge(tile), team, trigger, source, quantity, "Region")
    if progression is not None:
        return progression
    
    # Progress the tile quest
    # print(f"Tile challenge id: {db.get_tile_challenge(tile)}")
    progression = progress_quest(db.get_tile_challenge(tile), team, trigger, source, quantity, "Tile")
    if progression is not None:
        return progression

    # Progress the coin quest
    # print(f"Coin challenge id: {db.get_coin_challenge(tile)}")
    progression = progress_quest(db.get_coin_challenge(tile), team, trigger, source, quantity, "Coin")
    if progression is not None:
        return progression

    return None

def parse_tile_race_submission(type, rsn, discordId, source, item, price, quantity):
    # Check if the submission is between the start and end time
    current_time = datetime.now()
    start_time = db.get_start_time()
    end_time = db.get_end_time()
    # print(current_time, start_time, end_time)
    if current_time < start_time or current_time > end_time:
        print(f"Submission from {rsn} is outside of the start and end time")
        return

    # Check if the user list cache needs to be refreshed
    global lastUserListRefresh, tileRaceUserList
    global firstRefresh
    # if the price * quantity is greater than 100,000 then log it
    if price * quantity > 100000:
        print(f"{rsn} <@{discordId}> submitted a drop worth {price * quantity} gp: {item} from {source}")

    # Check if the cache is older than 10 minutes
    if (datetime.now() - lastUserListRefresh).total_seconds() > 600 or firstRefresh:
        # Refresh the cache
        print("Refreshing user list cache")
        tileRaceUserList = db.get_tile_race_full_user_list()
        if tileRaceUserList is None:
            print("There are no users in the user list!!!")
            return None
        tileRaceUserList = [x.lower() for x in tileRaceUserList]

        lastUserListRefresh = datetime.now()

    # # Check if the user is in the user list cache
    if rsn.lower() not in tileRaceUserList:
        return None

    # Parse the submission to see if it is an item drop or kc trigger
    # Oh, we already do this in the check above so this is redundant :D

    # Check if the trigger list cache needs to be refreshed
    global lastTriggerListRefresh, triggerList

    # Check if the cache is older than 10 minutes
    if (datetime.now() - lastTriggerListRefresh).total_seconds() > 600 or firstRefresh:
        # Refresh the cache
        triggerList = db.get_tile_race_full_trigger_list()
        triggerList = [x.lower() for x in triggerList]
        # print(f"Trigger list: {triggerList}")

        lastTriggerListRefresh = datetime.now()
    # Check if the trigger is in the trigger list cache

    firstRefresh = False
    trigger = item.lower()
    # Check to see if it matches regex
    match = re.match("sword completed in: [0-9]+m [0-9]+s at quality: ([0-9]+).*", trigger)
    if match:
        trigger = "sword quality"
        quantity = int(match.group(1))

    if trigger not in triggerList:
        return None

    print(f"Trigger {trigger} found in trigger list")

    # Update the progress of the team based on the submission
    # Grab the team from the user
    team = db.get_team(discordId)
    if team == 0:
        # Try again with username if discordId is not found
        team = db.get_team_with_username(rsn)
        if team == 0:
            print(f"Could not find team for user {rsn} with discordId {discordId}")
            return None
        else:
            print(f"Team {db.get_team_name(team)} found for user {rsn} with discordId {discordId} using username")
    else:
        print(f"Team {db.get_team_name(team)} found for user {rsn} with discordId {discordId}")


    if db.is_team_ready(team) or db.is_team_rolling(team):
        # print(f"Team {db.get_team_name(team)} is rolling")
        return None

    # Process the trigger for the team
    # print(team, trigger, source, quantity)
    progression = progress_team(team, trigger, source, quantity, rsn)

    # Check to see if the team has completed a quest or not
    if progression is not None:
        # If a quest has been completed, update the team with their rewards and return the message and thread id
        print(progression)
        return progression

    return None

    if not is_user_in_race(rsn):
        return None

    item = item.lower()
    team = db.get_team(discordId)
    rolling = db.is_team_ready(team)
    if rolling: # Team needs to roll first
        return None

    tile = db.get_team_tile(team)
    if tile is None or tile == -1:
        return None
    
    if type == "MANUAL":
        type = "LOOT"

    # blockers = db.get_blockers(team)
    # if len(blockers) > 0:
    #       # grab the last blocker
    #       last_blocker = blockers[-1]
    #       # parse the blocker
    #       blocker_name = last_blocker["name"]
    #       if "repeat" in last_blocker:
    #           blocker_tile = last_blocker["repeat"]


    # Get the tile from index
    tile_data = db.get_tile_data(tile)
    tile_name = tile_data["tile_name"]

    # Checks if the CHAT is a KC
    if type == "CHAT":
        match = re.match(KC_REGEX, item)
        if match:
            type = "KC"
            item = parse_kc_type(item.lower())
            quantity = int(match.group(1))

    submit = False
    submit_message = ""

    # Parse for side quest triggers
    side_triggers = tile_data["side_triggers"]

    for trigger in side_triggers:
        if trigger["type"] == "DROP":
            # Loop through all the triggers
            for t in trigger["trigger"]:
                # Grab the item and the source if there is one
                if ":" not in t:
                    if item.lower() == t.lower():
                        db.record_drop(rsn, team, discordId, item, source, price, quantity)
                        submit = add_side_quest_progress(team, tile, item, trigger, quantity)
                        if submit:
                            submit_message += f"@{team} has completed a side quest: with {quantity}x {item} from {source}\n"
                else:
                    i, s = t.split(":")
                    if item.lower() == i.lower() and source.lower() == s.lower():
                        db.record_drop(rsn, team, discordId, item, source, price, quantity)
                        submit = add_side_quest_progress(team, tile, item, trigger, quantity)
                        if submit:
                            submit_message += f"@{team} has completed a side quest: with {quantity}x {item} from {source}\n"
        elif trigger["type"] == "KC":
            # loop through all the triggers
            for t in trigger["trigger"]:
                if ":" not in t:
                    if item.lower() == t.lower():
                        db.record_kc(rsn, team, discordId, item)
                        submit = add_side_quest_progress(team, tile, item, trigger)
                        if submit:
                            submit_message += f"@{team} has completed a side quest: {item} has been slain!\n"
                else:
                    i, progress = t.split(":")
                    if item.lower() == i.lower():
                        db.record_kc(rsn, team, discordId, item)
                        submit = add_side_quest_progress(team, tile, item, trigger, int(progress))
                        if submit:
                            submit_message += f"@{team} has completed a side quest: {item} has been slain!\n"
        elif trigger["type"] == "CHAT":
            for t in trigger["trigger"]:
                match = re.match(t, item)
                if match:
                    # check if there are groups
                    if len(match.groups()) > 0:
                        value = int(match.group(1))
                    else:
                        value = 1
                    db.record_chat(rsn, team, discordId, t, value)

                    submit = add_side_quest_progress(team, tile, t, trigger, value)
                    if submit:
                        submit_message += f"@{team} has completed a side quest for: {tile_name}\n"
        elif trigger["type"] == "XP":
            # Yeah idk lmao
            pass

    # Parse for main triggers
    main_triggers = tile_data["main_triggers"]

    for trigger in main_triggers:
        if trigger["type"] == "DROP":
            # Loop through all the triggers
            for t in trigger["trigger"]:
                # Grab the item and the source if there is one
                if ":" not in t:
                    if item.lower() == t.lower():
                        db.record_drop(rsn, team, discordId, item, source, price, quantity)
                        submit = add_main_quest_progress(team, tile, item, trigger, quantity)
                        if submit:
                            submit_message += f"@{team} has completed a main quest: with {quantity}x {item} from {source}\n"
                else:
                    i, s = t.split(":")
                    if item.lower() == i.lower() and source.lower() == s.lower():
                        db.record_drop(rsn, team, discordId, item, source, price, quantity)
                        submit = add_main_quest_progress(team, tile, item, trigger, quantity)
                        if submit:
                            submit_message += f"@{team} has completed a main quest: with {quantity}x {item} from {source}\n"
        elif trigger["type"] == "KC":
            # loop through all the triggers
            for t in trigger["trigger"]:
                if ":" not in t:
                    if item.lower() == t.lower():
                        db.record_kc(rsn, team, discordId, item)
                        submit = add_main_quest_progress(team, tile, item, trigger)
                        if submit:
                            submit_message += f"@{team} has completed a main quest: {item} has been slain!\n"
                else:
                    i, progress = t.split(":")
                    if item.lower() == i.lower():
                        db.record_kc(rsn, team, discordId, item)
                        submit = add_main_quest_progress(team, tile, item, trigger, int(progress))
                        if submit:
                            submit_message += f"@{team} has completed a main quest: {item} has been slain!\n"
        elif trigger["type"] == "CHAT":
            for t in trigger["trigger"]:
                match = re.match(t, item)
                if match:
                    # check if there are groups
                    if len(match.groups()) > 0:
                        value = int(match.group(1))
                    else:
                        value = 1
                    db.record_chat(rsn, team, discordId, t, value)

                    submit = add_main_quest_progress(team, tile, t, trigger, value)
                    if submit:
                        submit_message += f"@{team} has completed the quest: {tile_name}\n"
        elif trigger["type"] == "XP":
            # Yeah idk lmao
            pass

    # Need to check if the drop is a pet or a tome of fire for auto completion of tile
    if type == "PET" or item == "tome of fire (uncharged)" or item == "golden tench":
        # Check if the team is ready
        if not db.is_team_ready(team):
            db.complete_tile(team, tile)
        db.add_stars(team, 1)

        submit = True
        submit_message += f"@{team} has completed the tile: {tile_data['tile_name']} with a: {item} from {source}!!!!\n"

    if submit == True:
        return {
            "message": submit_message,
            "thread_id": THREAD_ID,
        }
    return None
