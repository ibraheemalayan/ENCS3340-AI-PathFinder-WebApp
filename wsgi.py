# used only in production enviroment

import sys, os

sys.path.insert(0, "/var/www/ENCS3340-AI-PathFinder-WebApp")
sys.path.insert(1, "/var/www/venvs/route_finder_virtual_env_py3.9/lib/python3.9/site-packages")

from finder_app import create_app

application = create_app()

application.debug = True