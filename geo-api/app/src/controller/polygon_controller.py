from flask import request
from flask_restx import Resource

from ..util.dto import PolygonDTO
from ..service.polygon_service import add_polygons, get_all

api = PolygonDTO.api
_polygon = PolygonDTO.polygon


@api.route('')
class PolygonsCollection(Resource):

    @api.expect([_polygon], validate=True)
    @api.response(201, 'Polygons successfully added')
    @api.doc('adding polygon')
    def post(self):
        """Adding new polygons"""
        data = request.json
        return add_polygons(data=data)

    @api.doc('get the id of each cluster and the id of its neighbours')
    def get(self):
        """Get the id of each cluster and the id of its neighbors"""
        polygons = get_all()
        if not polygons:
            api.abort(400)
        else:
            return polygons

