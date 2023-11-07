from flask import Flask

from routes.default import route_default
from routes.reload_cache import reload_cache

app = Flask(__name__)

app.register_blueprint(route_default, url_prefix = '/')
app.register_blueprint(reload_cache, url_prefix = '/reload_cache')

if __name__ == '__main__':
  app.run(debug = True)
