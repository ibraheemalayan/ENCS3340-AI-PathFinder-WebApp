from finder_app.path_algos.models import load_graph_and_cities
from flask import g

g.G, g.city_dict, g.full_g = load_graph_and_cities()

