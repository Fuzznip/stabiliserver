from flask import Blueprint, jsonify
from sheets import refresh_cache

reload_cache = Blueprint("reload_cache", __name__)

@reload_cache.route('', methods = [ 'POST' ])
def handle_request():
  refresh_cache()
  return jsonify({"message": "Cache reloaded"})
