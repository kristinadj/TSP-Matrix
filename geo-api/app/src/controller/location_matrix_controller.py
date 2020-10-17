from flask_restx import Resource

from ..util.dto import LocationsMatrixDTO
from ..service.matrix_service import get_cross_locations_data, get_location_links_data, get_poi_links_data
from ..service.location_service import get_poi_ids


api = LocationsMatrixDTO.api


@api.route('/crossLocationLinks/neighbourPolygons')
class CrossLocationsData(Resource):

    @api.doc('data on distance/duration between cross locations from neighbouring polygons')
    def get(self):
        """Data on distance/duration between cross locations from neighbouring polygons"""
        response = get_cross_locations_data()
        return response

@api.route()
class PoiLinksData(Resource):

    @api.doc('data on distance/duration between POI locations within a polygon')
    def get(self, polygon_id):
        """Data on distance/duration between POI locations within a polygon"""
        poi_ids = get_poi_ids(polygon_id)
        poi_links = get_poi_links_data(polygon_id)

        response = {
            'polygonId': polygon_id,
            'poi_ids': poi_ids,
            'poi_links': poi_links
        }
        return response


@api.route()
class LocationsLinksData(Resource):

    @api.doc('data on distance/duration between cross locations, POI and cross locations and \
              vice versa within a polygon')
    def get(self, polygon_id):
        """Data on distance/duration between cross locations, POI and cross locations and \
              vice versa within a polygon"""
        location_links = get_location_links_data(polygon_id)

        response = {
            'polygonId': polygon_id,
            'location_links': location_links
        }
        return response

api.add_resource(PoiLinksData, '/poiLinks/<int:polygon_id>')
api.add_resource(LocationsLinksData, '/locationLinks/<int:polygon_id>')