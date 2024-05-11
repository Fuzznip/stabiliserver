import psycopg
from psycopg_pool import ConnectionPool
from psycopg.types.json import Jsonb

from dotenv import load_dotenv
load_dotenv()
import os

import json

dbpool = ConnectionPool(conninfo = os.getenv("DATABASE_URL"))

def ensure_tile_db():
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Create tiles table
      cur.execute("CREATE TABLE IF NOT EXISTS tiles (tile_id int PRIMARY KEY, tile_name TEXT, main_triggers jsonb[], side_triggers jsonb[], extra jsonb)")
      conn.commit()

def create_tile(tile_id, tile_name, main_triggers, side_triggers, extra):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Create a new tile
      cur.execute("INSERT INTO tiles (tile_id, tile_name, main_triggers, side_triggers, extra) VALUES (%s, %s, %s, %s, %s)", (tile_id, tile_name, Jsonb(main_triggers), Jsonb(side_triggers), Jsonb(extra)))
      conn.commit()

def update_tile(tile_id, tile_name, main_triggers, side_triggers, extra):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Update a tile
      cur.execute("UPDATE tiles SET tile_name = %s, main_triggers = %s, side_triggers = %s, extra = %s WHERE tile_id = %s", (tile_name, main_triggers, side_triggers, Jsonb(extra), tile_id))
      conn.commit()

def get_tile_data(tile_id):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Get the tile from the table
      cur.execute("SELECT tile_name, main_triggers, side_triggers, extra FROM tiles WHERE tile_id = %s", (tile_id, ))
      value = cur.fetchone()
      return {"tile_name": value[0], "main_triggers": value[1], "side_triggers": value[2], "extra": value[3]} if value is not None else None

def ensure_drops_db():
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Create drops table
      cur.execute("CREATE TABLE IF NOT EXISTS drops (drop_id SERIAL PRIMARY KEY, rsn TEXT, team TEXT, discord_id TEXT, item TEXT, source TEXT, value INT, quantity INT, total INT, type TEXT, timestamp TIMESTAMP)")
      conn.commit()

def add_drop(rsn, team, discord_id, item, source, value, quantity, total, type):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Add a drop to the table
      cur.execute("INSERT INTO drops (rsn, team, discord_id, item, source, value, quantity, total, type, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())", (rsn, team, discord_id, item, source, value, quantity, total, type))
      conn.commit()

def record_kc(rsn, team, discord_id, source):
  add_drop(rsn, team, discord_id, "killcount", source, 0, 1, 0, "KC")

def record_chat(rsn, team, discord_id, item, quantity):
  add_drop(rsn, team, discord_id, item, "chat", 0, quantity, 0, "CHAT")

def record_drop(rsn, team, discord_id, item, source, value, quantity):
  add_drop(rsn, team, discord_id, item, source, value, quantity, value * quantity, "DROP")

def get_user(discordId):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Get the user from the table
      cur.execute("SELECT username FROM users WHERE discord_id = %s", (discordId, ))
      value = cur.fetchone()
      return value[0] if value is not None else None

def get_user_from_username(username):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Get the user from the table
      cur.execute("SELECT discord_id FROM users WHERE username @> %s", ([username], ))
      value = cur.fetchone()
      return value[0] if value is not None else None

def get_team(discordId):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Get the team from the table
      cur.execute("SELECT team FROM teams WHERE discord_ids @> %s", ([discordId], ))
      value = cur.fetchone()
      return value[0] if value is not None else None

def get_team_tile(team):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Get the team from the table
      cur.execute("SELECT tile FROM teams WHERE team = %s", (team, ))
      value = cur.fetchone()
      return value[0] if value is not None else None
    
def add_stars(team, count):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Add stars to the team
      cur.execute("UPDATE teams SET stars = stars + %s WHERE team = %s", (count, team))
      conn.commit()

def add_coins(team, coins):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Add coins to the team
      cur.execute("UPDATE teams SET coins = coins + %s WHERE team = %s", (coins, team))
      conn.commit()

def set_coins(team, coins):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Add coins to the team
      cur.execute("UPDATE teams SET coins = %s WHERE team = %s", (coins, team))
      conn.commit()

def get_coin_count(team):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Get the team from the table
      cur.execute("SELECT coins FROM teams WHERE team = %s", (team, ))
      value = cur.fetchone()
      return value[0] if value is not None else None

def get_main_progress(team, tile):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Get the main progress from the table as a json
      cur.execute("SELECT tile_progress FROM teams WHERE team = %s", (team, ))
      value = json.dumps(cur.fetchall())
      value_dict = json.loads(value)[0][0]
      if value_dict is None:
        return None
      
      # loop through value tuple
      if str(tile) not in value_dict:
        return {}
      
      return value_dict[str(tile)]

def get_side_progress(team, tile):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Get the side progress from the table as a json
      cur.execute("SELECT side_progress FROM teams WHERE team = %s", (team, ))
      value = json.dumps(cur.fetchall())
      value_dict = json.loads(value)[0][0]
      if value_dict is None:
        return None
      
      # loop through value tuple
      if str(tile) not in value_dict:
        return {}
      
      return value_dict[str(tile)]

def save_main_progress(team, tile, main_progress):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Save the side progress to the table, adding the field if it doesn't exist
      cur.execute("UPDATE teams SET tile_progress = jsonb_set(tile_progress, %s, %s) WHERE team = %s", ([str(tile)], json.dumps(main_progress), team))
      conn.commit()

def save_side_progress(team, tile, side_progress):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Save the side progress to the table, adding the field if it doesn't exist
      cur.execute("UPDATE teams SET side_progress = jsonb_set(side_progress, %s, %s) WHERE team = %s", ([str(tile)], json.dumps(side_progress), team))
      conn.commit()

def complete_tile(team, tile):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Complete the tile
      cur.execute("UPDATE teams SET ready = true WHERE team = %s", (team, ))
      # Reset the "Roll Modifier" and "Roll Size" fields in the team
      cur.execute("UPDATE teams SET roll_size = 4, roll_modifier = 0, WHERE team = %s", (team, ))

      # Reset the "gained" field in the side progress
      # Get the side progress from the table as a json
      cur.execute("SELECT side_progress FROM teams WHERE team = %s", (team, ))
      value = json.dumps(cur.fetchall())
      value_dict = json.loads(value)[0][0]
      if value_dict and str(tile) in value_dict:
        for key in value_dict[str(tile)]:
          value_dict[str(tile)][key]["gained"] = 0
        cur.execute("UPDATE teams SET side_progress = jsonb_set(side_progress, %s, %s) WHERE team = %s", ([str(tile)], json.dumps(value_dict[str(tile)]), team))

      # Reset the "value" field in the main progress
      # Get the main progress from the table as a json
      cur.execute("SELECT tile_progress FROM teams WHERE team = %s", (team, ))
      value = json.dumps(cur.fetchall())
      value_dict = json.loads(value)[0][0]
      if value_dict and str(tile) in value_dict:
        for key in value_dict[str(tile)]:
          value_dict[str(tile)][key]["value"] = 0
        cur.execute("UPDATE teams SET tile_progress = jsonb_set(tile_progress, %s, %s) WHERE team = %s", ([str(tile)], json.dumps(value_dict[str(tile)]), team))

      conn.commit()

def is_team_ready(team):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Get the team from the table
      cur.execute("SELECT ready FROM teams WHERE team = %s", (team, ))
      value = cur.fetchone()
      return value[0] if value is not None else None

def get_blockers(team):
  with dbpool.connection() as conn:
    with conn.cursor() as cur:
      # Get the team from the table
      cur.execute("SELECT tile_blockers FROM teams WHERE team = %s", (team, ))
      value = cur.fetchone()
      return value[0] if value is not None else None