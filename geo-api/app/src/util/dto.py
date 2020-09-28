from flask_restx import Namespace, fields


class PolygonDTO:
    api = Namespace('Polygon', description='Polygon related operations')
    polygon = api.model('polygon', {
        'name': fields.String(required=True, description='polygon name'),
        'coordinates': fields.List(fields.List(fields.Float(required=True, descrption='coordinates - lat, lon')))
    })


class LocationDTO:
    api = Namespace('Location', description='Location related operations')
    location = api.model('location', {
        'name': fields.String(required=True, description='location name'),
        'lat': fields.Float(required=True, description='latitude'),
        'lon': fields.Float(required=True, description='longitude'),
        'is_cross_location': fields.Boolean(required=True, description="flag to describe is it cross location or POI")
    })


class GenerateLocationsMatrixDTO:
    api = Namespace('GenerateLocationsMatrix', description='Operations for generating locations matrix')


class LocationsMatrixDTO:
    api = Namespace('LocationsMatrix', description='Operations for fetching data from locations matrix')