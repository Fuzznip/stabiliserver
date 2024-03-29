from flask import Blueprint, jsonify, request
from utils.sheets import submit, should_submit, should_submit_screenshot, get_thread_id_list
from dotenv import load_dotenv
load_dotenv()
import os
import requests
import json

drop_submission_route = Blueprint("stability", __name__)

# function to parse death data
def parse_death(data):
  rsn = data['playerName']
  # Check if killerName exists
  if 'killerName' not in data['extra']:
    print("DEATH - " + rsn)
  else:
    print("DEATH - " + rsn + " died to " + data['extra']['killerName'])
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return False

# function to parse collection data
def parse_collection(data):
  print("COLLECTION")
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return False

# function to parse level data
def parse_level(data):
  print("LEVEL")
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return False

# function to parse loot data
# example data:
# {
#   "content": "%USERNAME% has looted: \n\n%LOOT%\nFrom: %SOURCE%",
#   "extra": {
#     "items": [
#       {
#         // type of this object is SerializedItemStack
#         "id": 1234,
#         "quantity": 1,
#         "priceEach": 42069,
#         // priceEach is the GE price of the item
#         "name": "Some item"
#       }
#     ],
#     "source": "Giant rat",
#     "category": "NPC",
#     "killCount": 60
#   },
#   "type": "LOOT",
#   "playerName": "your rsn",
#   "embeds": []
# }
def parse_loot(data):
  screenshotItems = []

  # Get rsn
  rsn = data['playerName']
  # Check if discordUser exists
  if 'discordUser' not in data:
    discordId = "None"
  else:
    discordId = data['discordUser']['id']
  source = data['extra']['source']

  # Get item list
  items = data['extra']['items']
  # Loop through items
  for item in items:
    # Get item name
    itemName = item['name']
    # Get item price
    itemPrice = item['priceEach']
    # Get item quantity
    itemQuantity = item['quantity']
    # Get item total
    itemTotal = item['priceEach'] * item['quantity']

    # Convert name to lowercase
    itemNameLower = itemName.lower()
    
    # Check if item is in the item list
    if should_submit(itemNameLower, source):
      # Submit item to database
      submit(rsn, discordId, source, itemName, itemPrice, itemQuantity, "LOOT")
      print("LOOT: " + rsn + " - " + itemName + " (" + source + ")")

      if should_submit_screenshot(itemNameLower, source):
        screenshotItems.append(itemName)

  return screenshotItems

# function to parse slayer data
def parse_slayer(data):
  print("SLAYER")
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return False

# function to parse quest data
def parse_quest(data):
  questList = [
    "Monkey Madness II",
    "Dragon Slayer II",
    "Song of the Elves",
    "Desert Treasure II - The Fallen Empire",
    "Legends' Quest",
    "Monkey Madness I",
    "Desert Treasure I",
    "Mourning's End Part I",
    "Mourning's End Part II",
    "Swan Song",
    "Dream Mentor",
    "Grim Tales",
    "Making Friends with My Arm",
    "The Fremennik Exiles",
    "Sins of the Father",
    "A Night at the Theatre",
    "Beneath Cursed Sands",
    "Secrets of the North",
  ]

  rsn = data['playerName']
  # Check if discordUser exists
  if 'discordUser' not in data:
    discordId = "None"
  else:
    discordId = data['discordUser']['id']

  questName = data['extra']['questName']

  if questName in questList:
    submit(rsn, discordId, "QUEST", questName, 0, 1, "QUEST")
    print("QUEST: " + rsn + " - " + questName)
    return [questName]

  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return []

# function to parse clue data
def parse_clue(data):
  screenshotItems = []
  # print data prettyfied
  
  rsn = data['playerName']
  # Check if discordUser exists
  if 'discordUser' not in data:
    discordId = "None"
  else:
    discordId = data['discordUser']['id']
  clueType = data['extra']['clueType']
  items = data['extra']['items']

  for item in items:
    # Get item name
    itemName = item['name']
    # Get item price
    itemPrice = item['priceEach']
    # Get item quantity
    itemQuantity = item['quantity']
    # Get item total
    itemTotal = item['priceEach'] * item['quantity']

    # Convert name to lowercase
    itemNameLower = itemName.lower()

    # Check if item is in the item list
    if should_submit(itemNameLower, clueType):
      # Submit item to database
      submit(rsn, discordId, clueType, itemName, itemPrice, itemQuantity, "CLUE")
      print("CLUE: " + rsn + " - " + itemName + " (" + clueType + ")")

      if should_submit_screenshot(itemNameLower, clueType):
        # Disable screenshotting for now
        # screenshotItems.append(itemName)
        pass

  return screenshotItems

# function to parse kill count data
def parse_kill_count(data):
  print("KILL_COUNT")
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return False

# function to parse combat achievement data
def parse_combat_achievement(data):
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  rsn = data['playerName']
  achievement = data['extra']['task']
  tier = data['extra']['tier']

  print("COMBAT_ACHIEVEMENT: " + rsn + " - " + achievement + " (" + tier + ")")
  return []

# function to parse pet data
def parse_pet(data):
  # print data prettyfied
  rsn = data['playerName']
  pet = data['extra']['petName']
  # Check if discordUser exists
  if 'discordUser' not in data:
    discordId = "None"
  else:
    discordId = data['discordUser']['id']
  submit(rsn, discordId, "PET", pet, 0, 1, "PET")
  print("PET: " + rsn + " - " + pet)
  return [pet]

# function to parse speedrun data
def parse_speedrun(data):
  print("SPEEDRUN")
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return False

# function to parse barbarian assault gamble data
def parse_barbarian_assault_gamble(data):
  print("BARBARIAN_ASSAULT_GAMBLE")
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return False

# function to parse player kill data
def parse_player_kill(data):
  print("PLAYER_KILL")
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return False

# function to parse group storage data
def parse_group_storage(data):
  print("GROUP_STORAGE")
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return False

# function to parse grand exchange data
def parse_grand_exchange(data):
  print("GRAND_EXCHANGE")
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return False

# function to parse trade data
def parse_trade(data):
  print("TRADE")
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return False

# function to parse leagues area data
def parse_leagues_area(data):
  print("LEAGUES_AREA")
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return False

# function to parse leagues relic data
def parse_leagues_relic(data):
  print("LEAGUES_RELIC")
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return False

# function to parse leagues task data
def parse_leagues_task(data):
  print("LEAGUES_TASK")
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return False

# function to parse login data
def parse_login(data):
  print("LOGIN")
  # print data prettyfied
  # print(json.dumps(data, indent = 2))
  return False

# function to delegate parsing to its own function basing on the 'type' data
def parse_json_data(json_data):
  data = json.loads(json_data)

  # types are: 'DEATH', 'COLLECTION, 'LEVEL', 'LOOT', 'SLAYER', 'QUEST', 
  # 'CLUE', 'KILL_COUNT', 'COMBAT_ACHIEVEMENT', 'PET', 'SPEEDRUN', 'BARBARIAN_ASSAULT_GAMBLE', 
  # 'PLAYER_KILL', 'GROUP_STORAGE', 'GRAND_EXCHANGE', 'TRADE', 'LEAGUES_AREA', 'LEAGUES_RELIC',
  # 'LEAGUES_TASK', and 'LOGIN'

  if 'type' in data:
    type = data['type']
    if type == 'DEATH':
      return parse_death(data)
    elif type == 'COLLECTION':
      return parse_collection(data)
    elif type == 'LEVEL':
      return parse_level(data)
    elif type == 'LOOT':
      return parse_loot(data)
    elif type == 'SLAYER':
      return parse_slayer(data)
    elif type == 'QUEST':
      return parse_quest(data)
    elif type == 'CLUE':
      return parse_clue(data)
    elif type == 'KILL_COUNT':
      return parse_kill_count(data)
    elif type == 'COMBAT_ACHIEVEMENT':
      return parse_combat_achievement(data)
    elif type == 'PET':
      return parse_pet(data)
    elif type == 'SPEEDRUN':
      return parse_speedrun(data)
    elif type == 'BARBARIAN_ASSAULT_GAMBLE':
      return parse_barbarian_assault_gamble(data)
    elif type == 'PLAYER_KILL':
      return parse_player_kill(data)
    elif type == 'GROUP_STORAGE':
      return parse_group_storage(data)
    elif type == 'GRAND_EXCHANGE':
      return parse_grand_exchange(data)
    elif type == 'TRADE':
      return parse_trade(data)
    elif type == 'LEAGUES_AREA':
      return parse_leagues_area(data)
    elif type == 'LEAGUES_RELIC':
      return parse_leagues_relic(data)
    elif type == 'LEAGUES_TASK':
      return parse_leagues_task(data)
    elif type == 'LOGIN':
      return parse_login(data)
    else:
      print(f"Unknown type: {type}")
  else:
    print(f"Unknown data: {data}")

  return []

@drop_submission_route.route('', methods = [ 'POST' ])
def handle_request():
  data = request.form
  image_required = False

  if 'payload_json' in data:
    json_data = data['payload_json']
    result = parse_json_data(json_data)
    if result:
      image_required = True

  thread_id_list = get_thread_id_list()

  if 'file' in request.files and image_required and len(thread_id_list) > 0:
    file = request.files['file']
    # Take payload data and image data and send it to WEBHOOK env variable
    webhook = os.environ.get("WEBHOOK")

    # Send the file to webhook
    data = json.loads(json_data)
    # for each item in result, send a webhook
    embeds = [
      {
        'author': data['embeds'][0]['author'],
        'description': '',
        'image': {
          'url': 'attachment://lootImage.png'
        }
      }
    ]

    # For each item in result, add a line to the embed's description
    for item in result:
      embeds[0]['description'] += f"{item}\n"

    # Remove the last newline character
    if len(embeds[0]['description']) > 0:
      embeds[0]['description'] = embeds[0]['description'][:-1]

    # Save the image to memory
    file.save("lootImage.png")

    for thread_id in thread_id_list:
      # Load the image from the file
      imageData = open("lootImage.png", "rb")

      files = {
        'file': ('lootImage.png', imageData, 'image/png')
      }
      
      payload = {
        'embeds': embeds
      }

      payload_link = webhook + '?thread_id=' + thread_id
      result = requests.post(payload_link, data = {'payload_json': json.dumps(payload)}, files = files)

      try:
        result.raise_for_status()
      except requests.exceptions.HTTPError as err:
        print(err)

  if result:
    return jsonify({"message": "Drop successfully submitted"})
  return jsonify({"message": "No action recorded"})
