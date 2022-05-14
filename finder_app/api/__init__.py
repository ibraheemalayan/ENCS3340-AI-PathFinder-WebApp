from flask import Blueprint, current_app, request, url_for

from finder_app.utils import json_res, is_json_client
from finder_app.path_algos.models import load_graph_and_cities, straight_line_distance
from finder_app.path_algos import astar_path, path_length


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/request_analyzer")
def request_analyzer():
    """
    Endpoint -> Returns data and headers of the request, used for debugging connection
    """

    res = {
        "data": request.get_data().__str__(),
        "server": request.server,
        "host": request.host,
        "request": request.__str__(),
        "SERVER_NAME": current_app.config["SERVER_NAME"],
        "headers": request.headers.__str__(),
    }
    
    if is_json_client():
        res["json"] = request.json

    # deepcode ignore XSS: <sent as json>
    return json_res(status=res)


@main_blueprint.route("/list_cities")
def list_cities():
    
    g, cities_dict = load_graph_and_cities()
    
    return json_res(code=200, cities=cities_dict)


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
        return json_res(code=400, message="the source or the destination city was not in the graph")
    
    path = astar_path(g, source=src, destination=dest, heuristic=straight_line_distance, mode=mode)
    
    accumulated_cost, step_lenghts=path_length(g, path, mode=mode)
    
    return json_res(code=200, path=path, accumulated_cost=accumulated_cost, step_costs=step_lenghts)