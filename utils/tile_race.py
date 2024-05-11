import re

import utils.db as db

from dotenv import load_dotenv
load_dotenv()
import os

THREAD_ID = os.environ.get("THREAD_ID", 1232048775405764789)

KC_REGEX = "your [\w\W]+ count is: ([0-9]+)\."
COIN_TO_STAR_THRESHOLD = 10
MAX_SIDE_QUEST_COINS = 8

def is_user_in_race(rsn):
  # lower case name first
  userId = db.get_user_from_username(rsn.lower())
  if userId is None:
    return False

  return not db.get_team(userId) is None

def parse_kc_type(item: str) -> str:
  if "tombs of amascut" in item:
    if "tombs of amascut: entry mode" in item:
      return "tombs of amascut entry mode"
    elif "tombs of amascut: expert mode" in item:
      return "tombs of amascut expert mode"
    return "tombs of amascut"
  elif "chambers of xeric" in item:
    if  "chambers of xeric challenge mode" in item:
      return "chambers of xeric challenge mode"
    return "chambers of xeric"
  elif "theatre of blood" in item:
    if "theatre of blood: entry mode" in item:
      return "theatre of blood entry mode"
    elif "theatre of blood: hard mode" in item:
      return "theatre of blood hard mode"
    return "theatre of blood"
  elif "giant mole" in item:
    return "giant mole"
  elif "scurrius" in item:
    return "scurrius"
  elif "tzkal-zuk" in item:
    return "tzkal-zuk"
  elif "tztok-jad" in item:
    return "tztok-jad"
  elif "agility pyramid" in item:
    return "agility pyramid"
  elif "agility arena" in item:
    return "agility arena"
  else:
    return "Not Implemented"

def add_side_quest_progress(team, tile, item, trigger, progress = 1):
  completion = False
  # Check if the count for the trigger is met
  trigger_count = trigger["count"]
  # get the current count for the trigger from the database
  side_progress = db.get_side_progress(team, tile)

  if item in side_progress:
    side_progress[item]["value"] = int(side_progress[item]["value"]) + progress
  else:
    side_progress[item] = {}
    side_progress[item]["value"] = progress
  current_count = side_progress[item]["value"]

  if current_count >= trigger_count:
    side_coins_gained = 0
    for i in side_progress:
      if "gained" in side_progress[i]:
        side_coins_gained += side_progress[i]["gained"]

    if side_coins_gained >= MAX_SIDE_QUEST_COINS:
      return False

    trigger_points = trigger["points"]
    if "gained" in side_progress[item]:
      trigger_points = min(MAX_SIDE_QUEST_COINS - side_progress[item]["gained"], trigger_points)
      side_progress[item]["gained"] += trigger_points
    else:
      side_progress[item]["gained"] = trigger_points

    coins_count = db.get_coin_count(team) 
    if coins_count + trigger_points >= COIN_TO_STAR_THRESHOLD:
      db.set_coins(team, coins_count + trigger_points - COIN_TO_STAR_THRESHOLD)
      db.add_stars(team, 1)
    else:
      db.add_coins(team, trigger_points)
    
    side_progress[item]["value"] -= trigger_count
    completion = True

  db.save_side_progress(team, tile, side_progress)
  return completion

def add_main_quest_progress(team, tile, item, trigger, progress = 1):
  completion = False
  # Check if the count for the trigger is met
  trigger_count = trigger["count"]
  # get the current count for the trigger from the database
  main_progress = db.get_main_progress(team, tile)

  if item in main_progress:
    main_progress[item]["value"] = int(main_progress[item]["value"]) + progress
  else:
    main_progress[item] = {}
    main_progress[item]["value"] = progress

  current_count = 0
  for t in trigger["trigger"]:
    # get everything before ":" if there is one
    t = t.split(":")[0]
    if t.lower() in main_progress:
      current_count += main_progress[t.lower()]["value"]

  trigger_count = trigger["count"]
  if current_count >= trigger_count:
    db.complete_tile(team, tile)
    # add stars
    db.add_stars(team, trigger["points"])
    completion = True
  else:
    db.save_main_progress(team, tile, main_progress)

  return completion

def parse_tile_race_submission(type, rsn, discordId, source, item, price, quantity):
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
  #   # grab the last blocker
  #   last_blocker = blockers[-1]
  #   # parse the blocker
  #   blocker_name = last_blocker["name"]
  #   if "repeat" in last_blocker:
  #     blocker_tile = last_blocker["repeat"]


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
