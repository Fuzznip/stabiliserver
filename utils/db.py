import psycopg
from psycopg_pool import ConnectionPool

from dotenv import load_dotenv
load_dotenv()
import os

import json

dbpool = ConnectionPool(conninfo = os.getenv("DATABASE_URL"))

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
    
def record_drop(team, tile, rsn, discordId, item, source, price, quantity):
  pass

def record_kc(team, tile, rsn, discordId, source):
  pass

def record_chat(team, tile, rsn, discordId, t):
  pass

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

