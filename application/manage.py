# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server
from application import app

from flask_assets import ManageAssets
from application import assets_env

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0',
    port = 80)
)

manager.add_command("assets", ManageAssets(assets_env))

if __name__ == "__main__":
    manager.run()