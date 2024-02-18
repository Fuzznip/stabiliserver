from flask import Blueprint, jsonify, request
from utils.sheets import get_item_list, fuzzy_find_items
import json

item_list = Blueprint("item_list", __name__)

@item_list.route('', methods = [ 'GET' ])
def get_item_list():
  itemlist = get_item_list()
  return jsonify({ "items": itemlist })

@item_list.route('', methods = [ 'POST' ])
def add_item_list():
  itemlist = get_item_list()
  return jsonify({ "items": itemlist })

@item_list.route('', methods = [ 'DELETE' ])
def delete_item():
  value = fuzzy_find_items(request.args.get("item"))
  if value is not None:
    return jsonify({ "Item": value[0] })
  else:
    return jsonify({ "None": "Item not found" })

