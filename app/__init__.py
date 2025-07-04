from flask import Flask
from flask_restful import Api

from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    api = Api(app)

    from app.routes import initialize_routes
    initialize_routes(api)

    return app
