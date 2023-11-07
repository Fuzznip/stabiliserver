from flask import Flask
from dotenv import load_dotenv
load_dotenv()
import os

from routes.default import route_default
from routes.reload_cache import reload_cache

app = Flask(__name__)

app.register_blueprint(route_default, url_prefix = '/')
app.register_blueprint(reload_cache, url_prefix = '/reload_cache')

if __name__ == '__main__':
  from waitress import serve
  print("Starting...")
  port = os.environ.get('PORT', 8080)
  serve(app, host = "0.0.0.0", port = port)