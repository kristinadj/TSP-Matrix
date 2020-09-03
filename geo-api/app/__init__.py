from flask_restx import Api
from flask import Blueprint

from .src.controller.polygon_controller import api as polygon_namespace

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Geo API',
          version='1.0',
          description='...'
          )

api.add_namespace(polygon_namespace, path='/polygon')