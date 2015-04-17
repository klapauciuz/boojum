# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server
from config import app

manager = Manager(app)

# Turn on debugger by default and reloader
# to run server print "python manage.py run"
manager.add_command("run", Server(
    use_debugger=True,
    use_reloader=True,
    host='127.0.0.1',
    port=5000)
)


if __name__ == "__main__":
    manager.run()

