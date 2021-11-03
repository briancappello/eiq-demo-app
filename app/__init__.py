import os

from flask import Flask, request


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    configure_app(app)
    init_extensions(app)
    register_blueprints(app)

    return app


def configure_app(app: Flask):
    from . import config

    app.config.from_object(config.Config)

    @app.template_test(name='active')
    def is_endpoint_active(endpoint):
        return endpoint == request.endpoint

    if os.getenv('FLASK_ENV', '').lower() == 'test':
        app.config.from_object(config.TestConfig)


def init_extensions(app: Flask):
    from .extensions import csrf

    csrf.init_app(app)


def register_blueprints(app: Flask):
    from .views import bp

    app.register_blueprint(bp)
