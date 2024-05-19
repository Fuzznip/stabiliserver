from flask import Blueprint, jsonify
from utils.sheets import refresh_cache
import utils.db as db

tiles = Blueprint("tiles", __name__)
count = 0

@tiles.route('', methods = [ 'GET' ])
def handle_request():
  global count 
  tile_data = db.get_tiles()
  print("get request" + str(count))
  count += 1

  return jsonify(tile_data)
