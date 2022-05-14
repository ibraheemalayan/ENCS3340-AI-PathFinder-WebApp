from email.policy import default
from finder_app.path_algos import astar_path, path_length
from finder_app.path_algos.models import (load_graph_and_cities,
                                          straight_line_distance)
from finder_app.utils import is_json_client, json_res
from flask import current_app, request

from . import main_blueprint

import networkx as nx

#### TODOs
# * select algorithim
# * view nodes on map - done
# * view path on map
# * select edge limit slider (and provide explanation)
# * select heuristic (walking, arial)
# * implement UCS as bounus by setting heuristic to zero
# * deploy to encs3340.unv.ibraheemalyan.dev or proj1.encs3340.unv.ibraheemalyan.dev
# * heuristic table ( as a pop up or another page )

from flask_wtf.form import FlaskForm
from wtforms.widgets import NumberInput
from wtforms.fields import RadioField, StringField, IntegerField
from wtforms.validators import DataRequired, Length

class AlgorithimForm(FlaskForm):
    """ algorithim properties form"""

    src_city = StringField("Source City", validators=[DataRequired(), Length(1, 32)])
    dest_city = StringField("Destination City", validators=[DataRequired(), Length(1, 32)])
    
    
    algo = RadioField(
        "Algorithim",
        validators=[DataRequired()],
        choices=[("astar", "A Star"), ("bfs", "BFS"), ("ucs", "UCS"), ("greedy", "Greedy")],
        default="astar",
    )
    weight = RadioField(
        "Weight",
        validators=[DataRequired()],
        choices=[("driving_cost", ""), ("walking_cost", ""), ("areial_cost", "")],
        default="driving_cost"
    )
    
    heuristic = RadioField(
        "Heuristic",
        validators=[DataRequired()],
        choices=[("aerial_heuristic", ""), ("walking_heuristic", "")],
        default="aerial_heuristic"
    )
    
    cost_limit = IntegerField(
        "Cost Limit", validators=[DataRequired()], default=50000
    )
    

@main_blueprint.route("/load_graph")
def load_graph():

    g, cities_dict = load_graph_and_cities()

    return json_res(code=200, 
                    graph=nx.node_link_data(g), 
                    view_lat=31.438349,
                    view_lng=34.7004952,
                    view_zoom=10)

@main_blueprint.route("/get_path", methods=['POST'])
def get_path():
    
    
    algo_form: AlgorithimForm = AlgorithimForm()
    
    if algo_form.validate():
        return json_res(code=200, yes="working")
    
    err = []
    
    for field, errors in algo_form.errors.items():
        
        err.append({
            "name": algo_form[field].label.text,
            "error": ', '.join(errors)
        })
        
    return json_res(code=400, errors=err)
    

    g, cities_dict = load_graph_and_cities()

    return json_res(code=200, 
                    graph=nx.node_link_data(g), 
                    view_lat=31.438349,
                    view_lng=34.7004952,
                    view_zoom=10)


@main_blueprint.route("/path/astar/<string:src>/<string:dest>")
def get_astar_path(src: str, dest: str):

    cost_limit = request.args.get("cost_limit", type=int, default=50000)
    mode = request.args.get("mode", type=str, default="driving")

    if mode == "driving":
        mode = "driving_cost"
    else:
        mode = "walking_cost"

    g, cities_dict = load_graph_and_cities(cost_limit=cost_limit)

    if src not in g or dest not in g:
        return json_res(
            code=400, message="the source or the destination city was not in the graph"
        )

    path = astar_path(
        g, source=src, destination=dest, heuristic=straight_line_distance, mode=mode
    )

    accumulated_cost, step_lenghts = path_length(g, path, mode=mode)

    return json_res(
        code=200, path=path, accumulated_cost=accumulated_cost, step_costs=step_lenghts
    )
