from flask import Blueprint, request, jsonify
import json
from sheets import in_item_list, submit

route_default = Blueprint("default", __name__)

def process_json(jsonData) -> bool:
  jsonObj = json.loads(jsonData)

  # write to submission database if item is whitelisted
  items = jsonObj['extra']['items']
  submitted = False
  for item in items:
    itemName = item['name']
    itemValue = item['priceEach']
    if in_item_list(itemName):
      print(f"  Yeah {itemName} is in there. thats good")
      submit(jsonObj["playerName"], jsonObj["discordUser"]["id"], itemName, itemValue, item['quantity'])
    else:
      print(f"  Nah {itemName} isnt in there.")

  return submitted

@route_default.route('', methods = [ 'POST' ])
def handle_request():
  data = request.form

  success = False
  # Parse the payload (json data and non-screenshot stuff)
  if 'payload_json' in data:
    json_data = data['payload_json']
    print("Parsing json data...")
    # Process the JSON data
    success = process_json(json_data)

  # Parse screenshot (if it exists)
  # TODO: Fwd screenshot data to discord webhook on successful submission to database
  # if 'file' in request.files:
  #   file = request.files['file']
  #   print("Parsing image data...")
  #   # Process the file (e.g., save it)
  #   file.save("received_image.png")

  if success:
    return jsonify({"message": "Drop successfully submitted"})
  else:
    return jsonify({"message": "No drop submitted"})
