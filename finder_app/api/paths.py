from email.policy import default
from finder_app.path_algos import astar_path, path_length, greedy, BFS, UCS
from finder_app.path_algos.models import NoRouteException, load_graph_and_cities
from finder_app.path_algos.heuristics import straight_line_distance, walking_distance
from finder_app.utils import json_res
from flask import current_app, request, g

from . import main_blueprint

import networkx as nx

#### TODOs
# * deploy to encs3340.unv.ibraheemalyan.dev or proj1.encs3340.unv.ibraheemalyan.dev
# * fix BFS

from flask_wtf.form import FlaskForm
from wtforms.widgets import NumberInput
from wtforms.fields import RadioField, StringField, IntegerField
from wtforms.validators import DataRequired, Length

class AlgorithimForm(FlaskForm):
    """algorithim properties form"""

    src_city = StringField("Source City", validators=[DataRequired(), Length(1, 32)])
    dest_cities = StringField(
        "Destination Cities", validators=[DataRequired(), Length(1, 256)]
    )

    algo = RadioField(
        "Algorithim",
        validators=[DataRequired()],
        choices=[
            ("astar", "A Star"),
            ("bfs", "BFS"),
            ("ucs", "UCS"),
            ("greedy", "Greedy"),
        ],
        default="astar",
    )
    weight = RadioField(
        "Weight",
        validators=[DataRequired()],
        choices=[
            ("driving_cost", "Driving"),
            ("walking_cost", "Walking"),
            ("aerial_cost", "Aerial"),
        ],
        default="driving_cost",
    )

    heuristic = RadioField(
        "Heuristic",
        validators=[DataRequired()],
        choices=[("aerial_heuristic", ""), ("walking_heuristic", "")],
        default="aerial_heuristic",
    )

    cost_limit = IntegerField("Cost Limit", validators=[DataRequired()], default=70) # km


def choose_algo_get_path(algo_form: AlgorithimForm, src_city, dest_city):
    
    path, heuristic = None, None
    
    if algo_form.algo.data == "astar":
    
        if (
            algo_form.heuristic.data == "walking_heuristic"
            and algo_form.weight.data == "aerial_cost"
        ):
            return json_res(
                code=406,
                msg="Illegal options, walking distance is not an admissible heuristic when the cost is aerial distance",
            )

        heuristic = (
            straight_line_distance
            if algo_form.heuristic.data == "aerial_heuristic"
            else walking_distance
        )

        path = astar_path(
            g.G,
            source=src_city,
            destination=dest_city,
            heuristic=heuristic,
            mode=algo_form.weight.data,
        )

    elif algo_form.algo.data == "bfs":

        # mode and heuristic don't matter

        path = BFS(
            g.G,
            source=src_city,
            destination=dest_city,
        )

    elif algo_form.algo.data == "greedy":

        # mode doesn't matter

        heuristic = (
            straight_line_distance
            if algo_form.heuristic.data == "aerial_heuristic"
            else walking_distance
        )

        path = greedy(
            g.G,
            source=src_city,
            destination=dest_city,
            heuristic=heuristic,
        )

    else:
        # UCS
        # heuristic doesn't matter

        path = UCS(
            g.G,
            source=src_city,
            destination=dest_city,
            mode=algo_form.weight.data,
        )
        
    return path, heuristic

@main_blueprint.route("/load_graph/<int:cost_limit>")
@main_blueprint.route("/load_graph")
def load_graph(cost_limit=None):

    if not hasattr(g, "cost_limit"):
        g.cost_limit = 50000

    if cost_limit is not None:
        g.cost_limit = cost_limit * 1000

    g.G, g.city_dict, g.full_g = load_graph_and_cities(cost_limit=g.cost_limit)

    return json_res(
        code=200,
        graph=nx.node_link_data(g.full_g),
        view_lat=31.6782381,
        view_lng=34.7416939,
        view_zoom=10,
    )


@main_blueprint.route("/get_path", methods=["POST"])
def get_path():

    algo_form: AlgorithimForm = AlgorithimForm()

    if algo_form.validate():
        
        if not hasattr(g, "cost_limit"):
            g.cost_limit = algo_form.cost_limit.data * 1000

        g.G, g.city_dict, g.full_g = load_graph_and_cities(
            cost_limit=g.cost_limit
        )
        
        goals = algo_form.dest_cities.data.split(", ")
        
        for dest_city in goals :
            if dest_city not in g.city_dict:
                return json_res(
                code=404,
                error="a destination city was not found in the data set",
            )

        if (
            algo_form.src_city.data not in g.city_dict
        ):
            return json_res(
                code=404,
                error="the source city was not found in the data set",
            )

        path, heuristic = [], None
        
        src_city = algo_form.src_city.data
        
        try:
            
            for dest_city in goals:
                
                if len(path) > 0:
                    path.pop() # remove duplicated city
                
                
                temp_path, heuristic = choose_algo_get_path(algo_form, src_city, dest_city)
                path.extend(temp_path)
                
                src_city = dest_city
                
        except NoRouteException:
            
            if algo_form.algo.data == "greedy":
                return json_res(code=508, msg="Greedy search did not find the path after 100k iterations")
            return json_res(code=404, msg="No Path Found")

        
        mode = dict(algo_form.weight.choices)[algo_form.weight.data]
        algo = algo_form.algo.label.text
        
        goal_city = goals[-1]

        # heuristic_table
        if algo_form.algo.data == "astar" or algo_form.algo.data == "greedy":
            
            heuristic_table = []

            for city in g.city_dict.keys():
                heuristic_table.append(
                    {
                        "city_name": city,
                        "value": round(heuristic(city, goal_city))
                    }
                )
        else:
            heuristic_table = 0
            

        path_driving_accumlated_cost, path_driving_step_costs = path_length(g.G, path=path, mode="driving_cost")
        path_walking_accumlated_cost, path_walking_step_costs = path_length(g.G, path=path, mode="walking_cost")
        path_aerial_accumlated_cost, path_aerial_step_costs = path_length(g.G, path=path, mode="aerial_cost")
        
        accumulated_cost = path_driving_accumlated_cost
        steps_costs = path_driving_step_costs
        other_cost_1_name = "Walking"
        other_cost_1_value = path_walking_accumlated_cost
        other_cost_2_name = "Aerial"
        other_cost_2_value = path_aerial_accumlated_cost
        
        if mode == "Walking":
            accumulated_cost = path_walking_accumlated_cost
            steps_costs = path_walking_step_costs
            other_cost_1_name = "Driving"
            other_cost_1_value = path_driving_accumlated_cost
            other_cost_2_name = "Aerial"
            other_cost_2_value = path_aerial_accumlated_cost
        elif mode == "Aerial":
            accumulated_cost = path_aerial_accumlated_cost
            steps_costs = path_aerial_step_costs
            other_cost_1_name = "Driving"
            other_cost_1_value = path_driving_accumlated_cost
            other_cost_2_name = "Walking"
            other_cost_2_value = path_walking_accumlated_cost
            
            

        return json_res(
            code=200,
            mode=mode,
            algo=algo,
            path=path,
            accumulated_cost=accumulated_cost,
            steps_costs=steps_costs,
            other_cost_1_name=other_cost_1_name ,
            other_cost_1_value=other_cost_1_value,
            other_cost_2_name=other_cost_2_name ,
            other_cost_2_value=other_cost_2_value,
            heuristic_table=heuristic_table,
            
            # DEBUG
            
            path_driving_accumlated_cost=path_driving_accumlated_cost,
            path_walking_accumlated_cost=path_walking_accumlated_cost,
            path_aerial_accumlated_cost=path_aerial_accumlated_cost,
            path_driving_step_costs=path_driving_step_costs,
            path_walking_step_costs=path_walking_step_costs,
            path_aerial_step_costs=path_aerial_step_costs
        )

    err = []

    for field, errors in algo_form.errors.items():

        err.append({"name": algo_form[field].label.text, "error": ", ".join(errors)})

    return json_res(code=400, errors=err)
