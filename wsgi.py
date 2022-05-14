import sys, os

sys.path.insert(0, ".")

from finder_app import create_app

application = create_app()

application.debug = True