from flask import Blueprint, jsonify
from utils.sheets import refresh_cache

reload_cache = Blueprint("reload_cache", __name__)

@reload_cache.route('', methods = [ 'POST' ])
def handle_request():
  refresh_cache(force = True)
  return jsonify({"message": "Cache reloaded"})
