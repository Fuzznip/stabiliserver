from flask import Blueprint, request, jsonify
import json
from utils.sheets import in_item_list, submit

route_default = Blueprint("default", __name__)

@route_default.route('', methods = [ 'POST' ])
def handle_request():
  # Default route is deprecated
  pass
