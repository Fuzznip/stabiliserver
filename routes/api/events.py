from flask import Blueprint, jsonify
import utils.db as db

events = Blueprint("events", __name__)
count = 0

@events.route('', methods = [ 'GET' ])
def handle_request():
  global count 
  event_data = db.get_events()
  print("get request" + str(count))
  count += 1

  return jsonify(event_data)
