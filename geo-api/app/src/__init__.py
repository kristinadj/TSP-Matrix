from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

from .config import config_by_name

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)

    return app