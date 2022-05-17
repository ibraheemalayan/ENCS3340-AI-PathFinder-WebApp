import sys, os

sys.path.insert(0, "/var/www/ENCS3340-AI-PathFinder-WebApp")

from finder_app import create_app

application = create_app()

application.debug = True