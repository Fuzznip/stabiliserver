import re

import utils.db as db

THREAD_ID = "1232048775405764789"

# tile = {
#   "name": "name",
#   "main_triggers": [
#     {
#       "type": "DROP",
#       "trigger": [""],
#       "count": 1,
#       "points": 1,
#     }
#   ],
#   "side_triggers": [
#     {
#       "type": "DROP",
#       "trigger": [""],
#       "count": 1,
#       "points": 1,
#     }
#   ]
# }

raid_tile = {
  "name": "Raid!",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Avernic defender hilt", "Ghrazi rapier", "Sanguinesti staff (uncharged)", "Justiciar faceguard", "Justiciar legguards", "Scythe of vitur (uncharged)", "Sanguine ornament kit", "Holy ornament kit", "Sanguine dust"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Twisted ancestral colour kit", "Metamorphic dust", "Dexterous prayer scroll", "Arcane prayer scroll", "Twisted buckler", "Dragon hunter crossbow", "Ancestral hat", "Ancestral robe top", "Ancestral robe bottom", "Dinh's bulwark", "Dragon claws", "Elder maul", "Kodai insignia", "Twisted bow"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Lightbearer", "Osmumten's fang", "Elidinis' ward", "Masori mask", "Masori body", "Masori chaps", "Tumeken's shadow (uncharged)"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "KC",
      "trigger": ["Tombs of Amascut Expert mode:2", "Tombs of Amascut:1", "Chambers of Xeric:2", "Chambers of Xeric Challenge Mode:3", "Theatre of Blood:2", "Theatre of Blood Hard mode:3"],
      "count": 50,
      "points": 1,
    }
  ],
  "side_triggers": [
    {
      "type": "KC",
      "trigger": ["Giant Mole"],
      "count": 125,
      "points": 1,
    }
  ]
}

wilderness_tile = {
  "name": "Wilderness Bosses",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Dragon pickaxe:Callisto", "Dragon pickaxe:Artio", "Dragon pickaxe:Vet'ion", "Dragon pickaxe:Calvar'ion", "Dragon pickaxe:Venenatis", "Dragon pickaxe:Spindel"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Voidwaker hilt", "Voidwaker gem", "Voidwaker blade"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Fangs of venenatis", "Skull of vet'ion", "Claws of callisto"],
      "count": 1,
      "points": 1,
    }
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": ["Fedora"],
      "count": 1,
      "points": 4,
    }
  ]
}

dks_tile = {
  "name": "The Triumvirate",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Berserker ring", "Warrior ring", "Seers ring", "Archers ring"],
      "count": 3,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": ["Ancient page 1", "Ancient page 2", "Ancient page 3", "Ancient page 4"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Bandos page 1", "Bandos page 2", "Bandos page 3", "Bandos page 4"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Saradomin page 1", "Saradomin page 2", "Saradomin page 3", "Saradomin page 4"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Guthix page 1", "Guthix page 2", "Guthix page 3", "Guthix page 4"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Zamorak page 1", "Zamorak page 2", "Zamorak page 3", "Zamorak page 4"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Armadyl page 1", "Armadyl page 2", "Armadyl page 3", "Armadyl page 4"],
      "count": 1,
      "points": 1,
    },
  ]
}

gotr_tile = {
  "name": "Guardians of the Rift",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Abyssal pearl"],
      "count": 150,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": ["Catalytic talisman", "Abyssal needle", "Abyssal lantern", "Abyssal red dye", "Abyssal green dye", "Abyssal blue dye"],
      "count": 1,
      "points": 2,
    },
  ]
}

super_slayer_tile = {
  "name": "Super Slayer",
  "main_triggers": [
    {
      "type": "XP",
      "trigger": ["Slayer"],
      "count": 400000,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": ["Unsired", "Hydra's Claw", "Hydra Tail", "Hydra Leather", "Hydra's Fang", "Hydra's Eye", "Hydra's Heart", "Jar of Chemicals", "Alchemical Hydra Heads", "Eternal Crystal", "Primordial Crystal", "Pegasian Crystal", "Jar of Souls", "Smouldering Stone", "Black Tourmaline Core", "Granite Gloves", "Granite Ring", "Granite Hammer", "Jar of Stone", "Kraken Tentacle", "Trident of the Seas (full)", "Jar of Dirt", "Smoke Battlestaff", "Dragon Chainbody", "Jar of Smoke" ],
      "count": 1,
      "points": 2,
    },
  ]
}

dt2_tile = {
  "name": "Desert Treasure II",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Awakener's orb"],
      "count": 2,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Virtus mask", "Virtus robe top", "Virtus robe bottom"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Leviathan's lure", "Siren's staff", "Executioner's axe head", "Eye of the duke"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Ultor vestige", "Bellator vestige", "Venator vestige", "Magus vestige"],
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "KC",
      "trigger": [ "Agility Pyramid" ],
      "count": 25,
      "points": 1,
    },
  ]
}

gauntlet_tile = {
  "name": "The Gauntlet",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Crystal shard:The Gauntlet"],
      "count": 300,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Crystal armour seed", "Crystal weapon seed", "Enhanced crystal weapon seed"],
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "KC",
      "trigger": [ "Agility Arena" ],
      "count": 50,
      "points": 1,
    }
  ]
}

zulrah_tile = {
  "name": "Super Snake",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Tanzanite fang", "Magic fang", "Serpentine visage", "Uncut onyx", "Tanzanite mutagen", "Magma mutagen"],
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "KC",
      "trigger": ["Scurrius"],
      "count": 50,
      "points": 1,
    }
  ]
}

vorkath_tile = {
  "name": "Money Dragon",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Vorkath's head"],
      "count": 2,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Skeletal visage", "Jar of decay", "Draconic visage", "Bonecrusher necklace"],
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": ["Scaly blue dragonhide"],
      "count": 1,
      "points": 1,
    }
  ]
}

free_tile = {
  "name": "FREE!",
  "main_triggers": [],
  "side_triggers": [],
  "extra": {
    "free": True
  }
}

clue_tile = {
  "name": "Confounding Clues",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Ranger boots", "Holy sandals", "Wizard boots", "Spiked manacles", "Climbing boots (g)"],
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": ["Purple sweets"],
      "count": 20,
      "points": 1,
    }
  ]
}

tempoross_tile = {
  "name": "Tempoross",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Fish barrel", "Tackle box", "Big harpoonfish", "Tome of water (empty)", "Tiny tempor", "Dragon harpoon"],
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": ["Spirit flakes"],
      "count": 200,
      "points": 1,
    }
  ]
}

demonic_gorilla_tile = {
  "name": "Money Monkeys",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Zenyte shard", "Ballista limbs"],
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": ["Dragon javelin heads"],
      "count": 125,
      "points": 1,
    }
  ]
}

# TODO: Fix this to be number of swords as a KC trigger instead
muspah_tile = {
  "name": "Phantom of the Muspah",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Venator shard"],
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "CHAT",
      "trigger": [".*Sword completed in: [0-9]*m* *[0-9]+s at quality: ([0-9]+)"],
      "count": 2000,
      "points": 1,
    }
  ]
}

toa_tile = {
  "name": "Tombs of Amongus",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Lightbearer", "Osmumten's fang", "Elidinis' ward", "Masori mask", "Masori body", "Masori chaps", "Tumeken's shadow (uncharged)", "Tumeken's guardian"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "KC",
      "trigger": ["Tombs of Amascut:1", "Tombs of Amascut Expert mode:2"],
      "count": 50,
      "points": 1,
    }
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": ["Pharaoh's sceptre", "Pharaoh's sceptre (uncharged)"],
      "count": 1,
      "points": 8,
    }
  ]
}

tob_tile = {
  "name": "Theatre of Bussy",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Avernic defender hilt", "Ghrazi rapier", "Sanguinesti staff (uncharged)", "Justiciar faceguard", "Justiciar legguards", "Scythe of vitur (uncharged)", "Lil'zik", "Sanguine ornament kit", "Holy ornament kit", "Sanguine dust"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "KC",
      "trigger": ["Theatre of Blood Entry mode:2", "Theatre of Blood:6", "Theatre of Blood Hard mode:9"],
      "count": 120,
      "points": 1,
    }
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": ["Ahrim's hood", "Ahrim's robetop", "Ahrim's robeskirt", "Ahrim's staff", "Dharok's helm", "Dharok's platebody", "Dharok's platelegs", "Dharok's greataxe", "Guthan's helm", "Guthan's platebody", "Guthan's chainskirt", "Guthan's warspear", "Karil's coif", "Karil's leathertop", "Karil's leatherskirt", "Karil's crossbow", "Torag's helm", "Torag's platebody", "Torag's platelegs", "Torag's hammers", "Verac's helm", "Verac's brassard", "Verac's plateskirt", "Verac's flail"],
      "count": 1,
      "points": 1,
    },
  ]
}

# TODO: Add 5 coins for completing this tile with inferno cape
tzhaar_tile = {
  "name": "Trouble in TzHaar Town",
  "main_triggers": [
    {
      "type": "KC",
      "trigger": ["TzKal-Zuk"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "KC",
      "trigger": ["TzTok-Jad"],
      "count": 10,
      "points": 1,
    }
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": ["Toktz-xil-ul", "Toktz-xil-ak", "Toktz-xil-ek", "Toktz-mej-tal", "Toktz-ket-xil", "Tzhaar-ket-om", "Obsidian cape", "Obsidian helmet", "Obsidian platebody", "Obsidian platelegs"],
      "count": 1,
      "points": 1,
    }
  ]
}

colosseum_tile = {
  "name": "Down with Dizana",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Sunfire splinter"],
      "count": 50000,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Dizana's quiver"],
      "count": 1,
      "points": 1,
    }
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": ["Guild hunter headwear", "Guild hunter top", "Guild hunter legs", "Guild hunter boots"],
      "count": 1,
      "points": 2,
    }
  ]
}

cox_tile = {
  "name": "Chambers of Xeric",
  "main_triggers":[
    {
      "type": "DROP",
      "trigger": ["Twisted bow", "Dinh's bulwark", "Ancestral hat", "Ancestral robe top", "Ancestral robe bottom", "Dragon claws", "Elder maul", "Kodai insignia", "Twisted buckler", "Dragon hunter crossbow", "Dexterous prayer scroll", "Arcane prayer scroll", "Twisted ancestral colour kit", "Metamorphic dust"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "KC",
      "trigger": ["Chambers of Xeric:2", "Chambers of Xeric Challenge Mode:3"],
      "count": 40,
      "points": 1,
    }
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": ["Warm gloves", "Bruma torch", "Pyromancer hood", "Pyromancer garb", "Pyromancer robe", "Pyromancer boots", "Tome of fire (empty)", "Phoenix", "Dragon axe", "Magic seed", "Torstol seed"],
      "count": 1,
      "points": 1,
    }
  ]
}

# TODO: Add a +4 die for completing this tile with a nex item
gwd_tile = {
  "name": "God Wars Dungeon",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Bandos boots", "Bandos tassets", "Bandos chestplate", "Bandos hilt", "Armadyl helmet", "Armadyl chestplate", "Armadyl chainskirt", "Armadyl hilt", "Zamorakian spear", "Staff of the dead", "Zamorakian hilt", "Saradomin sword", "Saradomin hilt", "Armadyl crossbow", "Saradomin's Light"],
      "count": 1,
      "points": 1,
    },
    {
      "type": "DROP",
      "trigger": ["Torva full helm (damaged)", "Torva platebody (damaged)", "Torva platelegs (damaged)", "Nihil horn", "Zaryte vambraces", "Ancient hilt"],
      "count": 1,
      "points": 2,
    }
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": ["Ensouled aviansie head"],
      "count": 2,
      "points": 1,
    }
  ]
}

mop_tile = {
  "name": "Moons of Peril",
  "main_triggers": [
    {
      "type": "DROP",
      "trigger": ["Eclipse atlatl", "Eclipse moon helm", "Eclipse moon chestplate", "Eclipse moon tassets", "Dual macuahuitl", "Blood moon helm", "Blood moon chestplate", "Blood moon tassets", "Blue moon spear", "Blue moon helm", "Blue moon chestplate", "Blue moon tassets"],
      "count": 1,
      "points": 1,
    },
  ],
  "side_triggers": [
    {
      "type": "DROP",
      "trigger": ["Blood moon tassets", "Blue moon tassets"],
      "count": 1,
      "points": 1,
    }
  ]
}

tiles = [
  raid_tile, # 0
  wilderness_tile, # 1
  dks_tile, # 2
  gotr_tile, # 3
  super_slayer_tile, # 4
  dt2_tile, # 5
  gauntlet_tile, # 6
  zulrah_tile, # 7
  vorkath_tile, # 8
  free_tile, # 9
  clue_tile, # 10
  tempoross_tile, # 11
  demonic_gorilla_tile, # 12
  muspah_tile, # 13
  toa_tile, # 14
  tob_tile, # 15
  tzhaar_tile, # 16
  colosseum_tile, # 17
  cox_tile, # 18
  gwd_tile, # 19
  mop_tile # 20
]

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
    coins_count = db.get_coin_count(team)
    trigger_points = trigger["points"]
    if "gained" in side_progress:
      if side_progress[item]["gained"] == MAX_SIDE_QUEST_COINS:
        current_count = 0
      trigger_points = min(MAX_SIDE_QUEST_COINS - side_progress[item]["gained"], trigger_points)
      side_progress[item]["gained"] += trigger_points
    else:
      side_progress[item]["gained"] = trigger_points

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
  tile_data = tiles[tile]

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
            submit = add_side_quest_progress(team, tile, item, trigger)
            if submit:
              submit_message += f"@{team} has completed a side quest: with {quantity}x {item} from {source}\n"
        else:
          i, s = t.split(":")
          if item.lower() == i.lower() and source.lower() == s.lower():
            db.record_drop(rsn, team, discordId, item, source, price, quantity)
            submit = add_side_quest_progress(team, tile, item, trigger)
            if submit:
              submit_message += f"@{team} has completed a side quest: with {quantity}x {item} from {source}\n"
    elif trigger["type"] == "KC":
      # loop through all the triggers
      for t in trigger["trigger"]:
        if ":" not in t:
          if item.lower() == t.lower():
            db.record_kc(team, tile, rsn, discordId, item)
            submit = add_side_quest_progress(team, tile, item, trigger)
            if submit:
              submit_message += f"@{team} has completed a side quest: {item} has been slain!\n"
        else:
          i, progress = t.split(":")
          if item.lower() == i.lower():
            db.record_kc(team, tile, rsn, discordId, item)
            submit = add_side_quest_progress(team, tile, item, trigger, int(progress))
            if submit:
              submit_message += f"@{team} has completed a side quest: {item} has been slain!\n"
    elif trigger["type"] == "CHAT":
        for t in trigger["trigger"]:
          db.record_chat(team, tile, rsn, discordId, t)
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
            submit = add_main_quest_progress(team, tile, item, trigger)
            if submit:
              submit_message += f"@{team} has completed a main quest: with {quantity}x {item} from {source}\n"
        else:
          i, s = t.split(":")
          if item.lower() == i.lower() and source.lower() == s.lower():
            db.record_drop(rsn, team, discordId, item, source, price, quantity)
            submit = add_main_quest_progress(team, tile, item, trigger)
            if submit:
              submit_message += f"@{team} has completed a main quest: with {quantity}x {item} from {source}\n"
    elif trigger["type"] == "KC":
      # loop through all the triggers
      for t in trigger["trigger"]:
        if ":" not in t:
          if item.lower() == t.lower():
            db.record_kc(team, tile, rsn, discordId, item)
            submit = add_main_quest_progress(team, tile, item, trigger)
            if submit:
              submit_message += f"@{team} has completed a main quest: {item} has been slain!\n"
        else:
          i, progress = t.split(":")
          if item.lower() == i.lower():
            db.record_kc(team, tile, rsn, discordId, item)
            submit = add_main_quest_progress(team, tile, item, trigger, int(progress))
            if submit:
              submit_message += f"@{team} has completed a main quest: {item} has been slain!\n"
    elif trigger["type"] == "CHAT":
        for t in trigger["trigger"]:
          db.record_chat(team, tile, rsn, discordId, t)
    elif trigger["type"] == "XP":
      # Yeah idk lmao
      pass

  # Need to check if the drop is a pet or a tome of fire for auto completion of tile
  if type == "PET" or item == "tome of fire (uncharged)":
    # Check if the team is ready
    if not db.is_team_ready(team):
      db.complete_tile(team, tile)
    db.add_stars(team, 1)

    submit = True
    submit_message += f"@{team} has completed the tile: {tile_data['name']} with a PET: {item} from {source}!!!!\n"

  if submit == True:
    return {
      "message": submit_message,
      "thread_id": THREAD_ID,
    }
  return None
