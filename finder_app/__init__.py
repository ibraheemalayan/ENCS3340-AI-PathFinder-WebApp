''' app factory '''

from os import environ
from flask import Flask, g
from .config import Config, config_modes
from .patches import wtforms_json

config_mode = environ.get("MODE") or "development"
config: Config = config_modes[config_mode]


def create_app():
    
    app = Flask(__name__, subdomain_matching=True)

    config = config_modes[config_mode]

    app.config.from_object(config)
    config_modes[config_mode].init_app(app)

    wtforms_json.init()

    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app)

    # ########################################################

    from .api import main_blueprint as main_bp

    app.register_blueprint(main_bp)

    app.debug = True

    return app
