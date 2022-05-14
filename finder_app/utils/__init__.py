
from decimal import Decimal
from json import dumps

from flask import current_app, request


def serialize(obj):
    """JSON serializer for objects not serializable by default orjson dumps"""

    if isinstance(obj, Decimal):
        return str(obj)

    return obj.to_json()


def is_json_client() -> bool:
    try:
        return "application/json" in request.headers.get("Accept")
    except TypeError:
        return False


def json_res(code=200, **kwargs):

    kwargs["http_status_code"] = code

    response = current_app.response_class(
        response=dumps(kwargs, default=serialize),
        status=int(code),
        mimetype="application/json",
    )

    return response