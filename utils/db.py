import psycopg
from psycopg_pool import ConnectionPool
from psycopg.types.json import Jsonb

from dotenv import load_dotenv
load_dotenv()
import os

import json

# dbpool = ConnectionPool(conninfo = os.getenv("DATABASE_URL"))

def ensure_task_db():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Create tasks table
            cur.execute("CREATE TABLE IF NOT EXISTS sp2tasks (id SERIAL PRIMARY KEY, triggers INT[], quantity INT)")
            conn.commit()

def ensure_challenge_db():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Create challenges table
            cur.execute("CREATE TABLE IF NOT EXISTS sp2challenges (id SERIAL PRIMARY KEY, name TEXT, description TEXT, tasks INT[])")
            conn.commit()

def ensure_trigger_db():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Create triggers table
            cur.execute("CREATE TABLE IF NOT EXISTS sp2triggers (trigger_id SERIAL PRIMARY KEY, trigger TEXT, source TEXT)")
            conn.commit()

def ensure_tile_db():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Create tiles table
            cur.execute("CREATE TABLE IF NOT EXISTS sp2tiles (tile_id SERIAL PRIMARY KEY, tile_name TEXT, description TEXT, region_name TEXT, coin_challenge SERIAL references sp2challenges(id), task_challenge SERIAL references sp2challenges(id), region_challenge SERIAL references sp2challenges(id), has_star BOOLEAN, has_item_shop BOOLEAN, next_tiles INT[], position POINT)")
            conn.commit()

def ensure_global_challenges_list_db():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Create global challenges list table
            cur.execute("CREATE TABLE IF NOT EXISTS sp2globalchallenges (id SERIAL PRIMARY KEY, challenges INT)")
            conn.commit()

def ensure_team_db():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Create teams table
            cur.execute("CREATE TABLE IF NOT EXISTS sp2teams (team SERIAL PRIMARY KEY, team_name TEXT, team_image TEXT, previous_tile INT, current_tile INT, stars INT, coins INT, coins_gained_this_tile INT, items INT[], buffs INT[], debuffs INT[], progress jsonb, ready BOOLEAN, rolling BOOLEAN, main_die_sides INT, main_die_modifier INT, extra_dice_sides INT[], role_id TEXT, text_channel_id TEXT, voice_channel_id TEXT, is_on_random_tile BOOLEAN, random_challenge INT)")
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
            cur.execute("CREATE TABLE IF NOT EXISTS sp2game (game_id SERIAL PRIMARY KEY, game_name TEXT, global_challenge INT, total_tiles_completed INT, star_locations INT[], item_shop_locations INT[], start_time TIMESTAMP, end_time TIMESTAMP)")
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
            cur.execute("SELECT ARRAY_AGG(trigger) AS all_triggers FROM sp2triggers")
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

def get_global_challenge():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the global challenge from the table
            cur.execute("SELECT global_challenge FROM sp2game WHERE game_id = 1")
            value = cur.fetchone()
            return value[0] if value is not None else 0

def get_region_challenge(tile):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the region challenge from the given tile
            cur.execute("SELECT region_challenge FROM sp2tiles WHERE tile_id = %s", (tile, ))
            value = cur.fetchone()
            return value[0] if value is not None else -1

def get_tile_challenge(tile):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the tile challenge from the given tile
            cur.execute("SELECT task_challenge FROM sp2tiles WHERE tile_id = %s", (tile, ))
            value = cur.fetchone()
            return value[0] if value is not None else -1

def get_coin_challenge(tile):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the coin challenge from the given tile
            cur.execute("SELECT coin_challenge FROM sp2tiles WHERE tile_id = %s", (tile, ))
            value = cur.fetchone()
            return value[0] if value is not None else -1

def get_progress(team):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the progress from the team
            cur.execute("SELECT progress FROM sp2teams WHERE team = %s", (team, ))
            value = cur.fetchone()
            return value[0] if value is not None else {}

def get_task_quantity(task):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the quantity from the task
            cur.execute("SELECT quantity FROM sp2tasks WHERE id = %s", (task, ))
            value = cur.fetchone()
            return value[0] if value is not None else 1

def complete_challenge(team, coins, die):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Complete the challenge
            cur.execute("UPDATE sp2teams SET coins = coins + %s WHERE team = %s", (coins, team))
            cur.execute("UPDATE sp2teams SET main_die_sides = %s WHERE team = %s", (die, team))
            cur.execute("UPDATE sp2teams SET ready = true WHERE team = %s", (team, ))
            conn.commit()

def save_progress(team, progress):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Save the progress to the team
            cur.execute("UPDATE sp2teams SET progress = %s WHERE team = %s", (Jsonb(progress), team))
            conn.commit()

def save_task_progress(team, challenge, task, progress):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the current progress from the team
            cur.execute("SELECT progress FROM sp2teams WHERE team = %s", (team, ))
            value = cur.fetchone()
            current_progress = value[0] if value is not None else {}

            # Update the progress with the new task
            if str(challenge) not in current_progress:
                current_progress[str(challenge)] = {}

            current_progress[str(challenge)][str(task)] = progress

            # Save the progress to the team
            cur.execute("UPDATE sp2teams SET progress = %s WHERE team = %s", (Jsonb(current_progress), team))
            conn.commit()

def get_challenge_name(challenge):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the challenge name from the table
            cur.execute("SELECT name FROM sp2challenges WHERE id = %s", (challenge, ))
            value = cur.fetchone()
            return value[0] if value is not None else None

def is_team_ready(team):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the team from the table
            cur.execute("SELECT ready FROM sp2teams WHERE team = %s", (team, ))
            value = cur.fetchone()
            return value[0] if value is not None else None

def is_team_rolling(team):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the team from the table
            cur.execute("SELECT rolling FROM sp2teams WHERE team = %s", (team, ))
            value = cur.fetchone()
            return value[0] if value is not None else None

def get_team_name(team):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the team name from the table
            cur.execute("SELECT team_name FROM sp2teams WHERE team = %s", (team, ))
            value = cur.fetchone()
            return value[0] if value is not None else None

def increment_challenge_count():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Increment the challenge count
            cur.execute("UPDATE sp2game SET total_tiles_completed = total_tiles_completed + 1 WHERE game_id = 1")
            conn.commit()

def get_challenge_tasks(challenge):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the tasks from the challenge
            cur.execute("SELECT tasks FROM sp2challenges WHERE id = %s", (challenge, ))
            value = cur.fetchone()
            return value[0] if value is not None else []

def get_task_triggers(task):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the triggers from the task
            cur.execute("SELECT triggers FROM sp2tasks WHERE id = %s", (task, ))
            value = cur.fetchone()
            return value[0] if value is not None else []

def get_trigger(trigger):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the trigger from the table
            cur.execute("SELECT trigger FROM sp2triggers WHERE trigger_id = %s", (trigger, ))
            value = cur.fetchone()
            return value if value is not None else None

def add_coins(team, coins):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Add coins to the team
            cur.execute("UPDATE sp2teams SET coins = coins + %s WHERE team = %s", (coins, team))
            conn.commit()

def increment_coins_gained_this_tile(team, coins):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Increment the coins gained this tile
            cur.execute("UPDATE sp2teams SET coins_gained_this_tile = coins_gained_this_tile + %s WHERE team = %s", (coins, team))
            conn.commit()

def set_coins_gained_this_tile(team, coins):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Set the coins gained this tile
            cur.execute("UPDATE sp2teams SET coins_gained_this_tile = %s WHERE team = %s", (coins, team))
            conn.commit()

def get_start_time():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the start time from the table
            cur.execute("SELECT start_time FROM sp2game WHERE game_id = 1")
            value = cur.fetchone()
            return value[0] if value is not None else None

def get_end_time():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the end time from the table
            cur.execute("SELECT end_time FROM sp2game WHERE game_id = 1")
            value = cur.fetchone()
            return value[0] if value is not None else None

def set_main_die_modifier(team, modifier):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Set the main die modifier
            cur.execute("UPDATE sp2teams SET main_die_modifier = %s WHERE team = %s", (modifier, team))
            conn.commit()

def set_extra_dice(team, sides):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Set the extra dice sides
            cur.execute("UPDATE sp2teams SET extra_dice_sides = %s WHERE team = %s", (sides, team))
            conn.commit()

def get_coins_gained_this_tile(team):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the coins gained this tile from the table
            cur.execute("SELECT coins_gained_this_tile FROM sp2teams WHERE team = %s", (team, ))
            value = cur.fetchone()
            return value[0] if value is not None else 0

def get_global_challenges():
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Get the global challenges from the table as an array
            cur.execute("SELECT challenges FROM sp2globalchallenges")
            value = cur.fetchone()
            return value[0] if value is not None else []

def set_global_challenge(challenge):
    with dbpool.connection() as conn:
        with conn.cursor() as cur:
            # Set the global challenge
            cur.execute("UPDATE sp2game SET global_challenge = %s WHERE game_id = 1", (challenge, ))
            conn.commit()

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
