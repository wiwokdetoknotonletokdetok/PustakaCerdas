from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from pustakacerdas.config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    api = Api(app)

    with app.app_context():
        from pustakacerdas import models

    from pustakacerdas.routes import initialize_routes
    initialize_routes(api)

    return app
