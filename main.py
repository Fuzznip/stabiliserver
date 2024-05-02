from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
import os

from routes.reload_cache import reload_cache
from routes.drop_submission_route import drop_submission_route
from routes.bot_submission_route import bot_submission_route

app = Flask(__name__)
CORS(app)

app.register_blueprint(reload_cache, url_prefix = '/reload_cache')
app.register_blueprint(drop_submission_route, url_prefix = '/stability')
app.register_blueprint(bot_submission_route, url_prefix = '/stabilibot')

if __name__ == '__main__':
  from waitress import serve
  print("Starting server...")
  port = os.environ.get('PORT', 8080)
  host = os.environ.get('HOST', "0.0.0.0")
  serve(app, host = host, port = port)
