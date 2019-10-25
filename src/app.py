from flask import Flask
from flask_mongoengine import MongoEngine
from src import config

db = MongoEngine()


def create_app(config_class=config.Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    return app
