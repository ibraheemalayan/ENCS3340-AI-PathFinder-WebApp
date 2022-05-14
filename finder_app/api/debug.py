
from finder_app.utils import is_json_client, json_res
from flask import current_app, request

from . import main_blueprint


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
