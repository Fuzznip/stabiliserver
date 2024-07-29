from flask import Blueprint, jsonify, request
from utils.sheets import submit

from dotenv import load_dotenv
load_dotenv()
import os

import requests
import json

bot_submission_route = Blueprint("stabilibot", __name__)

@bot_submission_route.route('', methods = [ 'POST' ])
def handle_request():
  data = request.get_json()
  if data is None:
    return jsonify({ "error": "Invalid request" })

  output = submit(data["user"], format(data["discordId"], '.0f'), data["source"], data["item"], 0, 0, "MANUAL")
  screenshotItems = {}
  if output is not None:
    threadIds = output["threadList"]
    for threadId in threadIds:
      if threadId not in screenshotItems:
        screenshotItems[threadId] = []
      if "message" in output:
        screenshotItems[threadId].append(output["message"])
      else:
        screenshotItems[threadId].append(data["item"])

  print(screenshotItems)
  if screenshotItems:
    for threadId, itemList in screenshotItems.items():
      # for each item in result, send a webhook
      embeds = [
        {
          'author': {
            'name': data['user'],
          },
          'description': '',
          'image': {
            'url': data['attachment']
          }
        }
      ]

      # Join all items in itemList with a newline character separating them
      embeds[0]['description'] = "\n".join(itemList)
      print(embeds) 

      payload = {
        'embeds': embeds
      }

      payload_link = os.environ.get("WEBHOOK") + '?thread_id=' + threadId
      result = requests.post(payload_link, data = {'payload_json': json.dumps(payload)})

      try:
        result.raise_for_status()
      except requests.exceptions.HTTPError as err:
        print(err)
  
  if screenshotItems:
    return jsonify({ "message": "Submission received" }), 200
  return jsonify({ "message": "No action recorded" }), 200
