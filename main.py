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
from routes.api.tiles import tiles
from routes.api.tile import tile
from routes.api.event import event
from routes.api.events import events

app = Flask(__name__)
CORS(app)

# utils.db.ensure_drops_db()
# utils.db.ensure_tile_db()

app.register_blueprint(reload_cache, url_prefix = '/reload_cache')
app.register_blueprint(drop_submission_route, url_prefix = '/stability')
app.register_blueprint(bot_submission_route, url_prefix = '/stabilibot')
app.register_blueprint(tiles, url_prefix = '/tiles')
app.register_blueprint(tile, url_prefix = '/tile')
app.register_blueprint(events, url_prefix = '/events')
app.register_blueprint(event, url_prefix = '/event')

if __name__ == '__main__':
  from waitress import serve
  print("Starting server...")
  port = os.environ.get('PORT', 8080)
  host = os.environ.get('HOST', "0.0.0.0")
  serve(app, host = host, port = port)
