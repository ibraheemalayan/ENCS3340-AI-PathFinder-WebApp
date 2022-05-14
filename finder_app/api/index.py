
from finder_app.utils import is_json_client, json_res
from flask import current_app, request, render_template

from . import main_blueprint


@main_blueprint.route("/")
def index():
    """ Index """
    
    return render_template("index.html")