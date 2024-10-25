import psycopg
from psycopg_pool import ConnectionPool
from psycopg.types.json import Jsonb

from dotenv import load_dotenv
load_dotenv()
import os

import json

dbpool = ConnectionPool(conninfo = os.getenv("DATABASE_URL"))

def ensure_task_db():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Create tasks table
            cur.execute("CREATE TABLE IF NOT EXISTS sp2tasks (task_id SERIAL PRIMARY KEY, trigger TEXT, source TEXT, quantity INT)")
            conn.commit()

def ensure_tile_db():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Create tiles table
            cur.execute("CREATE TABLE IF NOT EXISTS sp2tiles (tile_id SERIAL PRIMARY KEY, tile_name TEXT, tile_tasks INT[], region_tasks INT[], coin_tasks INT[], has_star BOOLEAN, has_item_shop BOOLEAN, next_tiles INT[])")
            conn.commit()

def ensure_team_db():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Create teams table
            cur.execute("CREATE TABLE IF NOT EXISTS sp2teams (team SERIAL PRIMARY KEY, team_name TEXT, previous_tile INT, current_tile INT, stars INT, coins INT, items INT[], buffs INT[], debuffs INT[], tile_progress jsonb, ready BOOLEAN, main_die_sides INT, main_die_modifier INT, extra_dice_sides INT[])")
            conn.commit()

def ensure_user_db():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Create users table
            cur.execute("CREATE TABLE IF NOT EXISTS sp2users (discord_id TEXT PRIMARY KEY, usernames TEXT[], team SERIAL REFERENCES sp2teams(team))")
            conn.commit()

def ensure_game_db():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Create game data table
            cur.execute("CREATE TABLE IF NOT EXISTS sp2game (game_id SERIAL PRIMARY KEY, game_name TEXT, global_tasks INT[], total_tiles_completed INT, star_locations INT[], item_shop_locations INT[], start_time TIMESTAMP, end_time TIMESTAMP)")
            conn.commit()

def get_tile_race_full_user_list():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the full list of usernames in the game
            cur.execute("SELECT ARRAY_AGG(username) AS all_usernames FROM(SELECT UNNEST(usernames) AS username FROM sp2users) AS aggregated_usernames")
            value = cur.fetchall()
            return value[0][0] if value is not None else []

def get_tile_race_full_trigger_list():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the full list of triggers from all tiles in the game
            cur.execute("SELECT ARRAY_AGG(trigger) AS all_triggers FROM sp2tasks")
            value = cur.fetchall()
            return value[0][0] if value is not None else []

def get_team(discordId):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the team id from the table with the discord id
            cur.execute("SELECT team FROM sp2users WHERE discord_id = %s", (discordId, ))
            value = cur.fetchone()
            return value[0] if value is not None else 0

def get_team_with_username(username):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the team id from the table with the username
            cur.execute("SELECT team FROM sp2users WHERE %s = ANY(usernames)", (username, ))
            value = cur.fetchone()
            return value[0] if value is not None else 0

def get_team_tile(team):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the team's current tile from the table
            cur.execute("SELECT current_tile FROM sp2teams WHERE team = %s", (team, ))
            value = cur.fetchone()
            return value[0] if value is not None else 0

def get_tile_tasks(tile):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the tile tasks from the given tile
            cur.execute("SELECT tile_tasks FROM sp2tiles WHERE tile_id = %s", (tile, ))
            value = cur.fetchone()
            return value[0] if value is not None else []

def get_region_tasks(tile):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the region tasks from the given tile
            cur.execute("SELECT region_tasks FROM sp2tiles WHERE tile_id = %s", (tile, ))
            value = cur.fetchone()
            return value[0] if value is not None else []

def get_global_tasks():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the global tasks for the game
            cur.execute("SELECT global_tasks FROM sp2game WHERE game_id = 1")
            value = cur.fetchone()
            return value[0] if value is not None else []

def get_task_trigger(task):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the trigger from the task
            cur.execute("SELECT trigger FROM sp2tasks WHERE task_id = %s", (task, ))
            value = cur.fetchone()
            return value[0] if value is not None else ""

def get_task_source(task):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the source from the task
            cur.execute("SELECT source FROM sp2tasks WHERE task_id = %s", (task, ))
            value = cur.fetchone()
            return value[0] if value is not None else ""

def get_progress(team):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the progress from the team
            cur.execute("SELECT tile_progress FROM sp2teams WHERE team = %s", (team, ))
            value = cur.fetchone()
            return value[0] if value is not None else {}

def get_task_quantity(task):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the quantity from the task
            cur.execute("SELECT quantity FROM sp2tasks WHERE task_id = %s", (task, ))
            value = cur.fetchone()
            return value[0] if value is not None else 1


# def ensure_tile_db():
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
    #             # Create tiles table
#             cur.execute("CREATE TABLE IF NOT EXISTS tiles (tile_id int PRIMARY KEY, tile_name TEXT, main_triggers jsonb[], side_triggers jsonb[], extra jsonb)")
#             conn.commit()
#
# def create_tile(tile_id, tile_name, main_triggers, side_triggers, extra):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Create a new tile
#             cur.execute("INSERT INTO tiles (tile_id, tile_name, main_triggers, side_triggers, extra) VALUES (%s, %s, %s, %s, %s)", (tile_id, tile_name, Jsonb(main_triggers), Jsonb(side_triggers), Jsonb(extra)))
#             conn.commit()
#
# def update_tile(tile_id, tile_name, main_triggers, side_triggers, extra):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Update a tile
#             cur.execute("UPDATE tiles SET tile_name = %s, main_triggers = %s, side_triggers = %s, extra = %s WHERE tile_id = %s", (tile_name, main_triggers, side_triggers, Jsonb(extra), tile_id))
#             conn.commit()
#
# def get_tile_data(tile_id):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Get the tile from the table
#             cur.execute("SELECT tile_name, main_triggers, side_triggers, extra FROM tiles WHERE tile_id = %s", (tile_id, ))
#             value = cur.fetchone()
#             return {"tile_name": value[0], "main_triggers": value[1], "side_triggers": value[2], "extra": value[3]} if value is not None else None
#
# def ensure_drops_db():
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Create drops table
#             cur.execute("CREATE TABLE IF NOT EXISTS drops (drop_id SERIAL PRIMARY KEY, rsn TEXT, team TEXT, discord_id TEXT, item TEXT, source TEXT, value INT, quantity INT, total INT, type TEXT, timestamp TIMESTAMP)")
#             conn.commit()
#
# def add_drop(rsn, team, discord_id, item, source, value, quantity, total, type):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Add a drop to the table
#             cur.execute("INSERT INTO drops (rsn, team, discord_id, item, source, value, quantity, total, type, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())", (rsn, team, discord_id, item, source, value, quantity, total, type))
#             conn.commit()
#
# def record_kc(rsn, team, discord_id, source):
#     add_drop(rsn, team, discord_id, "killcount", source, 0, 1, 0, "KC")
#
# def record_chat(rsn, team, discord_id, item, quantity):
#     add_drop(rsn, team, discord_id, item, "chat", 0, quantity, 0, "CHAT")
#
# def record_drop(rsn, team, discord_id, item, source, value, quantity):
#     add_drop(rsn, team, discord_id, item, source, value, quantity, value * quantity, "DROP")
#
# def get_user(discordId):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Get the user from the table
#             cur.execute("SELECT username FROM users WHERE discord_id = %s", (discordId, ))
#             value = cur.fetchone()
#             return value[0] if value is not None else None
#
# def get_user_from_username(username):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Get the user from the table
#             cur.execute("SELECT discord_id FROM users WHERE username @> %s", ([username], ))
#             value = cur.fetchone()
#             return value[0] if value is not None else None
#
# def get_team(discordId):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Get the team from the table
#             cur.execute("SELECT team FROM teams WHERE discord_ids @> %s", ([discordId], ))
#             value = cur.fetchone()
#             return value[0] if value is not None else None
#
# def get_team_tile(team):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Get the team from the table
#             cur.execute("SELECT tile FROM teams WHERE team = %s", (team, ))
#             value = cur.fetchone()
#             return value[0] if value is not None else None
#         
# def add_stars(team, count):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Add stars to the team
#             cur.execute("UPDATE teams SET stars = stars + %s WHERE team = %s", (count, team))
#             conn.commit()
#
# def add_coins(team, coins):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Add coins to the team
#             cur.execute("UPDATE teams SET coins = coins + %s WHERE team = %s", (coins, team))
#             conn.commit()
#
# def set_coins(team, coins):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Add coins to the team
#             cur.execute("UPDATE teams SET coins = %s WHERE team = %s", (coins, team))
#             conn.commit()
#
# def get_coin_count(team):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Get the team from the table
#             cur.execute("SELECT coins FROM teams WHERE team = %s", (team, ))
#             value = cur.fetchone()
#             return value[0] if value is not None else None
#
# def get_main_progress(team, tile):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Get the main progress from the table as a json
#             cur.execute("SELECT tile_progress FROM teams WHERE team = %s", (team, ))
#             value = json.dumps(cur.fetchall())
#             value_dict = json.loads(value)[0][0]
#             if value_dict is None:
#                 return None
#             
#             # loop through value tuple
#             if str(tile) not in value_dict:
#                 return {}
#             
#             return value_dict[str(tile)]
#
# def get_side_progress(team, tile):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Get the side progress from the table as a json
#             cur.execute("SELECT side_progress FROM teams WHERE team = %s", (team, ))
#             value = json.dumps(cur.fetchall())
#             value_dict = json.loads(value)[0][0]
#             if value_dict is None:
#                 return None
#             
#             # loop through value tuple
#             if str(tile) not in value_dict:
#                 return {}
#             
#             return value_dict[str(tile)]
#
# def save_main_progress(team, tile, main_progress):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Save the side progress to the table, adding the field if it doesn't exist
#             cur.execute("UPDATE teams SET tile_progress = jsonb_set(tile_progress, %s, %s) WHERE team = %s", ([str(tile)], json.dumps(main_progress), team))
#             conn.commit()
#
# def save_side_progress(team, tile, side_progress):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Save the side progress to the table, adding the field if it doesn't exist
#             cur.execute("UPDATE teams SET side_progress = jsonb_set(side_progress, %s, %s) WHERE team = %s", ([str(tile)], json.dumps(side_progress), team))
#             conn.commit()
#
# def complete_tile(team, tile):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Complete the tile
#             cur.execute("UPDATE teams SET ready = true WHERE team = %s", (team, ))
#             # Reset the "Roll Modifier" and "Roll Size" fields in the team
#             cur.execute("UPDATE teams SET roll_modifier = 0 WHERE team = %s", (team, ))
#
#             # Reset the "gained" field in the side progress
#             # Get the side progress from the table as a json
#             cur.execute("SELECT side_progress FROM teams WHERE team = %s", (team, ))
#             value = json.dumps(cur.fetchall())
#             value_dict = json.loads(value)[0][0]
#             if value_dict and str(tile) in value_dict:
#                 for key in value_dict[str(tile)]:
#                     value_dict[str(tile)][key]["gained"] = 0
#                 cur.execute("UPDATE teams SET side_progress = jsonb_set(side_progress, %s, %s) WHERE team = %s", ([str(tile)], json.dumps(value_dict[str(tile)]), team))
#
#             # Reset the "value" field in the main progress
#             # Get the main progress from the table as a json
#             cur.execute("SELECT tile_progress FROM teams WHERE team = %s", (team, ))
#             value = json.dumps(cur.fetchall())
#             value_dict = json.loads(value)[0][0]
#             if value_dict and str(tile) in value_dict:
#                 for key in value_dict[str(tile)]:
#                     value_dict[str(tile)][key]["value"] = 0
#                 cur.execute("UPDATE teams SET tile_progress = jsonb_set(tile_progress, %s, %s) WHERE team = %s", ([str(tile)], json.dumps(value_dict[str(tile)]), team))
#
#             conn.commit()
#
# def is_team_ready(team):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Get the team from the table
#             cur.execute("SELECT ready FROM teams WHERE team = %s", (team, ))
#             value = cur.fetchone()
#             return value[0] if value is not None else None
#
# def get_blockers(team):
#     with dbpool.connection() as conn:
#         with conn.cursor() as cur:
#             # Get the team from the table
#             cur.execute("SELECT tile_blockers FROM teams WHERE team = %s", (team, ))
#             value = cur.fetchone()
#             return value[0] if value is not None else None
