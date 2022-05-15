
from finder_app.utils import is_json_client, json_res
from flask import g, render_template

from . import main_blueprint


@main_blueprint.route("/")
def index():
    """ Index """
    
    if not hasattr(g, "cost_limit"):
        g.cost_limit = 50000
    
    return render_template("index.html")