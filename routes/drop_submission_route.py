from flask import Blueprint, jsonify, request
from utils.sheets import submit
from dotenv import load_dotenv
load_dotenv()
import os
import requests
import json
import re

drop_submission_route = Blueprint("stability", __name__)

# function to parse death data
def parse_death(data) -> dict[str, list[str]]:
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
def parse_collection(data) -> dict[str, list[str]]:
    print("COLLECTION")
    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    return False

# function to parse level data
def parse_level(data) -> dict[str, list[str]]:
    print("LEVEL")
    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    return False

# function to parse loot data
# example data:
# {
#       "content": "%USERNAME% has looted: \n\n%LOOT%\nFrom: %SOURCE%",
#       "extra": {
#           "items": [
#               {
#                   // type of this object is SerializedItemStack
#                   "id": 1234,
#                   "quantity": 1,
#                   "priceEach": 42069,
#                   // priceEach is the GE price of the item
#                   "name": "Some item"
#               }
#           ],
#           "source": "Giant rat",
#           "category": "NPC",
#           "killCount": 60
#       },
#       "type": "LOOT",
#       "playerName": "your rsn",
#       "embeds": []
# }
def parse_loot(data) -> dict[str, list[str]]:
    screenshotItems: dict[str, list[str]] = {}

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

    if "hunters' loot sack" in source.lower():
        items.append({
            "name": "Hunter rumour",
            "priceEach": 0,
            "quantity": 1
        })

        source = "Hunter rumour"

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
        
        # Check if item is in the item list
        output = submit(rsn, discordId, source, itemName, itemPrice, itemQuantity, "LOOT")
        if output is not None:
            threadIds = output["threadList"]
            for threadId in threadIds:
                if threadId not in screenshotItems:
                    screenshotItems[threadId] = []
                if "message" in output:
                    screenshotItems[threadId].append(output["message"])
                else:
                    screenshotItems[threadId].append(itemName)

    return screenshotItems

# function to parse slayer data
def parse_slayer(data) -> dict[str, list[str]]:
    screenshotItems: dict[str, list[str]] = {}

    rsn = data['playerName']
    # Check if discordUser exists
    if 'discordUser' not in data:
        discordId = "None"
    else:
        discordId = data['discordUser']['id']
    print(data['extra']['slayerPoints'])
    # remove commas from slayerPoints
    pointsReceived = int(data['extra']['slayerPoints'].replace(",", ""))
    print(pointsReceived)
    # convert pointsReceived to int
    if int(pointsReceived) > 0:
        output = submit(rsn, discordId, "SLAYER", "Slayer point", 0, pointsReceived, "SLAYER")

        if output is not None:
            threadIds = output["threadList"]
            for threadId in threadIds:
                if threadId not in screenshotItems:
                    screenshotItems[threadId] = []
                if "message" in output:
                    screenshotItems[threadId].append(output["message"])
                else:
                    screenshotItems[threadId].append("Slayer Points")

        output = submit(rsn, discordId, "SLAYER", "Slayer task", 0, 1, "SLAYER")

        if output is not None:
            threadIds = output["threadList"]
            for threadId in threadIds:
                if threadId not in screenshotItems:
                    screenshotItems[threadId] = []
                if "message" in output:
                    screenshotItems[threadId].append(output["message"])
                else:
                    screenshotItems[threadId].append("Slayer Task")
    else:
        print("SLAYER - " + rsn + " received 0 Slayer Points from a task and was not counted")


    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    return screenshotItems

# function to parse quest data
def parse_quest(data) -> dict[str, list[str]]:
    # questList = [
    #       "Monkey Madness II",
    #       "Dragon Slayer II",
    #       "Song of the Elves",
    #       "Desert Treasure II - The Fallen Empire",
    #       "Legends' Quest",
    #       "Monkey Madness I",
    #       "Desert Treasure I",
    #       "Mourning's End Part I",
    #       "Mourning's End Part II",
    #       "Swan Song",
    #       "Dream Mentor",
    #       "Grim Tales",
    #       "Making Friends with My Arm",
    #       "The Fremennik Exiles",
    #       "Sins of the Father",
    #       "A Night at the Theatre",
    #       "Beneath Cursed Sands",
    #       "Secrets of the North",
    # ]

    screenshotItems: dict[str, list[str]] = {}

    rsn = data['playerName']
    # Check if discordUser exists
    if 'discordUser' not in data:
        discordId = "None"
    else:
        discordId = data['discordUser']['id']

    questName = data['extra']['questName']

    output = submit(rsn, discordId, "QUEST", questName, 0, 1, "QUEST")
    if output is not None:
        threadIds = output["threadList"]
        for threadId in threadIds:
            if threadId not in screenshotItems:
                screenshotItems[threadId] = []
            if "message" in output:
                screenshotItems[threadId].append(output["message"])
            else:
                screenshotItems[threadId].append(questName)

    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    return screenshotItems

# function to parse clue data
def parse_clue(data) -> dict[str, list[str]]:
    screenshotItems: dict[str, list[str]] = {}
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
        output = submit(rsn, discordId, clueType, itemName, itemPrice, itemQuantity, "CLUE")
        if output is not None:
            threadIds = output["threadList"]
            for threadId in threadIds:
                if threadId not in screenshotItems:
                    screenshotItems[threadId] = []
                if "message" in output:
                    screenshotItems[threadId].append(output["message"])
                else:
                    screenshotItems[threadId].append(itemName)

    return screenshotItems

# function to parse kill count data
def parse_kill_count(data) -> dict[str, list[str]]:
    print("KILL_COUNT")
    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    return False

# function to parse combat achievement data
def parse_combat_achievement(data) -> dict[str, list[str]]:
    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    rsn = data['playerName']
    achievement = data['extra']['task']
    tier = data['extra']['tier']

    print("COMBAT_ACHIEVEMENT: " + rsn + " - " + achievement + " (" + tier + ")")
    return []

# function to parse pet data
def parse_pet(data) -> dict[str, list[str]]:
    screenshotItems: dict[str, list[str]] = {}
    # print data prettyfied
    rsn = data['playerName']
    pet = data['extra']['petName']
    output = []
    # Check if discordUser exists
    if 'discordUser' not in data:
        discordId = "None"
    else:
        discordId = data['discordUser']['id']
    output = submit(rsn, discordId, "PET", pet, 0, 1, "PET")
    if output is not None:
        threadIds = output["threadList"]
        for threadId in threadIds:
            if threadId not in screenshotItems:
                screenshotItems[threadId] = []
            if "message" in output:
                screenshotItems[threadId].append(output["message"])
            else:
                screenshotItems[threadId].append(pet)

    return screenshotItems

# function to parse speedrun data
def parse_speedrun(data) -> dict[str, list[str]]:
    print("SPEEDRUN")
    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    return False

# function to parse barbarian assault gamble data
def parse_barbarian_assault_gamble(data) -> dict[str, list[str]]:
    print("BARBARIAN_ASSAULT_GAMBLE")
    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    return False

# function to parse player kill data
def parse_player_kill(data) -> dict[str, list[str]]:
    print("PLAYER_KILL")
    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    return False

# function to parse group storage data
def parse_group_storage(data) -> dict[str, list[str]]:
    print("GROUP_STORAGE")
    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    return False

# function to parse grand exchange data
def parse_grand_exchange(data) -> dict[str, list[str]]:
    print("GRAND_EXCHANGE")
    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    return False

# function to parse trade data
def parse_trade(data) -> dict[str, list[str]]:
    print("TRADE")
    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    return False

# function to parse leagues area data
def parse_leagues_area(data) -> dict[str, list[str]]:
    print("LEAGUES_AREA")
    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    return False

# function to parse leagues relic data
def parse_leagues_relic(data) -> dict[str, list[str]]:
    print("LEAGUES_RELIC")
    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    return False

# function to parse leagues task data
def parse_leagues_task(data) -> dict[str, list[str]]:
    print("LEAGUES_TASK")
    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    return False

def parse_chat(data) -> dict[str, list[str]]:
    screenshotItems: dict[str, list[str]] = {}
    # print(data)
    # Check if discordUser exists
    if 'discordUser' not in data:
        discordId = "None"
    else:
        discordId = data['discordUser']['id']

    def check_string_for_kc(item):
        KC_REGEX = "[\w\W]+: ([0-9,]+)\."
        match = re.match(KC_REGEX, item)
        if not match:
            return "Not Implemented"

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
        elif "scurrius" in item:
            return "scurrius"
        elif "giant mole" in item:
            return "giant mole"
        elif "sarachnis" in item:
            return "sarachnis"
        elif "king black dragon" in item:
            return "king black dragon"
        elif "phantom muspah" in item:
            return "phantom muspah"
        elif "kalphite queen" in item:
            return "kalphite queen"
        elif "vorkath" in item:
            return "vorkath"
        elif "phosani's nightmare" in item:
            return "phosani's nightmare"
        elif "nightmare" in item:
            return "nightmare"
        elif "wintertodt" in item:
            return "wintertodt"
        elif "tempoross" in item:
            return "tempoross"
        elif "rifts you have closed" in item:
            return "guardians of the rift"
        elif "alchemical hydra" in item:
            return "alchemical hydra"
        elif "colossal wyrm" in item:
            return "colossal wyrm"
        elif "zalcano" in item:
            return "zalcano"
        elif "araxxor" in item:
            return "araxxor"
        elif "thermonuclear smoke devil" in item:
            return "thermonuclear smoke devil"
        elif "grotesque guardians" in item:
            return "grotesque guardians"
        elif "kraken" in item:
            return "kraken"
        elif "cerberus" in item:
            return "cerberus"
        elif "abyssal sire" in item:
            return "abyssal sire"
        elif "nex" in item:
            return "nex"
        elif "hueycoatl" in item:
            return "hueycoatl"
        elif "lunar chest" in item:
            return "lunar chest"
        else:
            return "Not Implemented"

    kcString = check_string_for_kc(data['extra']['message'].lower())
    if kcString != "Not Implemented":
        output = submit(data['playerName'], discordId, kcString, kcString, 0, 1, "KC")
    else:
        output = submit(data['playerName'], discordId, "CHAT", data['extra']['message'], 0, 1, "CHAT")

    if output is not None:
        # print data prettyfied
        # print(json.dumps(data, indent = 2))
        threadIds = output["threadList"]
        for threadId in threadIds:
            if threadId not in screenshotItems:
                screenshotItems[threadId] = []
            if "message" in output:
                screenshotItems[threadId].append(output["message"])
            else:
                screenshotItems[threadId].append(data['extra']['message'])

    return screenshotItems

# function to parse login data
def parse_login(data) -> dict[str, list[str]]:
    print("LOGIN")
    # print data prettyfied
    # print(json.dumps(data, indent = 2))
    return False

# function to delegate parsing to its own function basing on the 'type' data
def parse_json_data(json_data) -> dict[str, list[str]]:
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
        elif type == 'CHAT':
            return parse_chat(data)
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
        try:
            result = parse_json_data(json_data)
        except Exception as e:
            print("Error parsing JSON data: " + str(e))
            print(json.dumps(json_data, indent = 2))
            return jsonify({"message": "Error parsing JSON data: " + str(e)})
        if result:
            image_required = True

    if 'file' in request.files and image_required:
        file = request.files['file']

        # Send the file to webhook
        data = json.loads(json_data)

        # Save the image to memory
        file.save("lootImage.png")

        print(result)

        for threadId, itemList in result.items():
            # for each item in result, send a webhook
            print(data)
            embeds = [
                {
                    'author': data['embeds'][0]['author'] if data['embeds'] is not None and len(data['embeds']) > 0 else {'name': 'Stabilibot'},
                    'description': '',
                    'image': {
                        'url': 'attachment://lootImage.png'
                    }
                }
            ]

            # Remove duplicate item names in item list
            itemList = list(set(itemList))

            # Join all items in itemList with a newline character separating them
            embeds[0]['description'] = "\n".join(itemList)
            print(embeds) 
            print(json_data)

            # Load the image from the file
            with open("lootImage.png", "rb") as imageData:
                files = {
                    'file': ('lootImage.png', imageData, 'image/png')
                }
                
                payload = {
                    'embeds': embeds
                }

                print(threadId)
                # print type of threadId
                print(type(threadId))
                # Take payload data and image data and send it to WEBHOOK env variable
                if threadId != "":
                    print("Posting to thread")
                    webhook = os.environ.get("FORUM_WEBHOOK")
                    payload_link = webhook + '?thread_id=' + threadId
                else:
                    print("Posting to webhook")
                    webhook = os.environ.get("CHANNEL_WEBHOOK")
                    payload_link = webhook
                result = requests.post(payload_link, data = {'payload_json': json.dumps(payload)}, files = files)
                print({"payload_json": json.dumps(payload)})

                try:
                    result.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    print(err)

    if result:
        return jsonify({"message": "Drop successfully submitted"})
    return jsonify({"message": "No action recorded"})
