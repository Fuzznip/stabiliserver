from flask import Blueprint, jsonify
from utils.sheets import refresh_cache
import utils.db as db

tile = Blueprint("tile", __name__)
count = 0

@tile.route('', methods = [ 'GET' ])
def handle_request():
  global count
  # get the tile id from the request
  tile_data = db.get_tiles()
  print("get request" + str(count))
  count += 1

  return jsonify(tile_data)
