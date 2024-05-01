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

  outputs = submit(data["user"], format(data["discordId"], '.0f'), data["source"], data["item"], 0, 0, "MANUAL")

  for output in outputs:
    url = os.environ.get("WEBHOOK") + "?thread_id=" + output
  
    embeds = [
      {
        'author': {
          'name': data["user"]
        },
        'description': data["item"],
        'image': {
          'url': data["attachment"]
        }
      }
    ]

    payload = {
      'embeds': embeds
    }

    result = requests.post(url, data = {'payload_json': json.dumps(payload)})

    try:
      result.raise_for_status()
    except requests.exceptions.HTTPError as err:
      print(err)
  
  if result:
    return jsonify({ "message": "Submission received" })
  return jsonify({ "message": "No action recorded" })