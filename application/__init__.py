from flask import Flask
app = Flask(__name__)

import json
CONFIG_FILE = 'config.json'
config = None
with open(CONFIG_FILE, 'r') as f:
    config = json.load(f)
# def get_config(key=None):
#     config = g.get('_config')
#     if not config:
#         with open(CONFIG_FILE, 'r') as f:
#             config = g._config = json.load(f)
#     if key:
#         config = config.get(key)
#     return config
# g.config = get_config


app.config.update(config)


# Setup static assets
from flask_assets import Environment
from webassets.loaders import PythonLoader as PythonAssetsLoader
import assets
assets_env = Environment(app)
assets_loader = PythonAssetsLoader(assets)
for name, bundle in assets_loader.load_bundles().iteritems():
    assets_env.register(name, bundle)

import scribd
scribd.config(app.config['SCRIBD_API_KEY'], app.config['SCRIBD_API_SECRET'])

# Setup Mongo Database
# from flask.ext.mongoengine import MongoEngine
# app.config["MONGODB_SETTINGS"] = {'DB': "my_tumble_log"}
# app.config["SECRET_KEY"] = "KeepThisS3cr3t"
# db = MongoEngine(app)

def register_blueprints(app):
    # Prevents circular imports
    from application.views import views
    app.register_blueprint(views)


register_blueprints(app)

if __name__ == '__main__':
    app.run()
