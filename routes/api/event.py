from flask import Blueprint, jsonify
import utils.db as db

event = Blueprint("event", __name__)
count = 0

@event.route('/<event_id>', methods = [ 'GET' ])
def handle_request(event_id):
  global count 
  print(event_id)
  event_data = db.get_event(event_id)
  print("get request" + str(count))
  count += 1

  return jsonify(event_data)
