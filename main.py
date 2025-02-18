from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
import os

import utils.db
import utils.tile_race

from routes.reload_cache import reload_cache
from routes.drop_submission_route import drop_submission_route
from routes.bot_submission_route import bot_submission_route

app = Flask(__name__)
CORS(app)

# utils.db.ensure_drops_db()
utils.db.ensure_task_db()
utils.db.ensure_challenge_db()
utils.db.ensure_trigger_db()
utils.db.ensure_tile_db()
utils.db.ensure_global_challenges_list_db()
utils.db.ensure_team_db()
utils.db.ensure_user_db()
utils.db.ensure_game_db()

app.register_blueprint(reload_cache, url_prefix = '/reload_cache')
app.register_blueprint(drop_submission_route, url_prefix = '/stability')
app.register_blueprint(bot_submission_route, url_prefix = '/stabilibot')

if __name__ == '__main__':
    from waitress import serve
    print("Starting server...")
    port = os.environ.get('PORT', 8080)
    host = os.environ.get('HOST', "0.0.0.0")
    serve(app, host = host, port = port)
