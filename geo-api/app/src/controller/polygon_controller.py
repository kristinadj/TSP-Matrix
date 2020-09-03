from flask import request
from flask_restx import Resource

from ..util.dto import PolygonDTO
from ..service.polygon_service import get_all, add_polygon, get_by_id

api = PolygonDTO.api
_polygon = PolygonDTO.polygon

@api.route('/')
class PolygonsCollection(Resource):
    
    @api.doc('all polygons')
    @api.marshal_list_with(_polygon, envelope='data')
    def get(self):
        """List of all polygons"""
        return get_all()


    @api.expect(_polygon, validate=True)
    @api.response(201, 'Polygon successfully created')
    @api.doc('create a new polygon')
    def post(self):
        """Creates a new polygon"""
        data = request.json
        return add_polygon(data=data)


@api.route('/<id>')
@api.param('id', 'polygon identifier')
@api.response(404, 'polygon not found')
class PolygonItem(Resource):

    @api.doc('get a polygon')
    @api.marshal_with(_polygon)
    def get(self, id):
        """Get a polygon given its identitfier"""
        polygon = get_by_id(id)
        if not polygon:
            api.abort(404)
        else:
            return polygon

