import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # FIXME deepcode ignore HardcodedNonCryptoSecret: <please specify a reason of ignoring this>
    SECRET_KEY = ';kjasicl4tiwueliaulascruyalkr'  # TODO regenerate

    SERVER_NAME = "p1.encs3340.unv.ibraheemalayan.dev"
    DOMAIN_NAME = "p1.encs3340.unv.ibraheemalayan.dev"

    SSL_REDIRECT = True

    # ######## Cookies ########

    WTF_CSRF_ENABLED = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):

    SERVER_NAME = "localhost:9000"
    DOMAIN_NAME = "localhost"

    DEBUG = True
    SSL_REDIRECT = False
    WTF_CSRF_ENABLED = False
    
    @staticmethod
    def init_app(app):
        pass


class RemoteDevelopmentConfig(DevelopmentConfig):

    SERVER_NAME = "p1.encs3340.unv.ibraheemalyan.dev"
    DOMAIN_NAME = "p1.encs3340.unv.ibraheemalyan.dev"

    SSL_REDIRECT = False

    @classmethod
    def init_app(cls, app):

        DevelopmentConfig.init_app(app)

        # log to stderr
        import logging

        gunicorn_error_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)

        app.logger.debug("RemoteDevelopmentConfig was loaded")


config_modes: dict[str, Config] = {
    "development": DevelopmentConfig,
    "remote_development": RemoteDevelopmentConfig,
    "raw": Config,
}
