from flask_restx import Resource

from ..util.dto import GenerateLocationsMatrixDTO
from ..service.matrix_service import generate_all_polygons, generate_neighbour_polygons

api = GenerateLocationsMatrixDTO.api


@api.route('/polygons')
class GenerateAllLocationsMatrix(Resource):

    @api.response(200, '')
    @api.doc('generating for locations inside same polygons')
    def post(self):
        """Generating matrix for all locations inside same polygon"""
        success = generate_all_polygons()

        if not success:
            api.abort(400)


@api.route('/neighbourPolygons')
class GenerateNeighbourCrossLocationsMatrix(Resource):

    @api.response(200, '')
    @api.doc('generating for cross locations in neighbour polygons')
    def post(self):
        """Generating matrix for cross locations in neighbour polygons"""
        success = generate_neighbour_polygons()

        if not success:
            api.abort(400)