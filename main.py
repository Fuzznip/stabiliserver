from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
import os

from routes.default import route_default
from routes.reload_cache import reload_cache
#from routes.item_list import item_list
from routes.drop_submission_route import drop_submission_route

app = Flask(__name__)
CORS(app)

#app.register_blueprint(route_default, url_prefix = '/')
app.register_blueprint(reload_cache, url_prefix = '/reload_cache')
#app.register_blueprint(item_list, url_prefix = '/item_list')
app.register_blueprint(drop_submission_route, url_prefix = '/stability')

if __name__ == '__main__':
  from waitress import serve
  print("Starting server...")
  port = os.environ.get('PORT', 8080)
  serve(app, host = "0.0.0.0", port = port)
