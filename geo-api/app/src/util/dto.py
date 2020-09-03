from flask_restx import Namespace, fields


class PolygonDTO:
    api = Namespace('polygon', description='Polygon related operations')
    polygon = api.model('polygon', {
        'name': fields.String(required=True, description='polygon name'),
        'geo': fields.String(required=True, descripiotn='geospatial data for polygon')
    })