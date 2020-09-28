from flask_restx import Api
from flask import Blueprint

from .src.controller.polygon_controller import api as polygon_namespace
from .src.controller.location_controller import api as location_namespace
from .src.controller.generate_location_matrix_controller import api as generate_matrix_namespace
from .src.controller.location_matrix_controller import api as matrix_namespace


blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Geo API',
          version='1.0',
          description='...'
          )

api.add_namespace(polygon_namespace, path='/polygon')
api.add_namespace(location_namespace, path='/location')
api.add_namespace(generate_matrix_namespace, path='/generateMatrix')
api.add_namespace(matrix_namespace, path='/matrix')