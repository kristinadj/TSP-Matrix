from flask_restx import Resource

from ..util.dto import LocationsMatrixDTO
from ..service.matrix_service import get_cross_locations_data, get_cross_locations_links_data, get_poi_links_data

api = LocationsMatrixDTO.api


@api.route('/crossLocation')
class CrossLocationsData(Resource):

    @api.doc('data on distance/duration between cross locations from neighbouring polygons')
    def get(self):
        """Data on distance/duration between cross locations from neighbouring polygons"""
        response = get_cross_locations_data()
        if not response:
            api.abort(400)
            
        return response


@api.route()
class CrossLocationsLinksData(Resource):

    @api.doc('data on distance/duration between cross locations within a polygon')
    def get(self, polygon_id):
        """Data on distance/duration between cross locations within a polygon"""
        cross_location_links = get_cross_locations_links_data(polygon_id)
        if not cross_location_links:
            api.abort(400)

        response = {
            'polygonId': polygon_id,
            'cross_location_links': cross_location_links
        }
        return response


@api.route()
class POILocationsLinksData(Resource):

    @api.doc('data on distance/duration between POI locations within a polygon')
    def get(self, polygon_id):
        """Data on distance/duration between POI locations within a polygon"""
        poi_links = get_poi_links_data(polygon_id)
        if not poi_links:
            api.abort(400)
        
        response = {
            'polygonId': polygon_id,
            'poi_location_links': poi_links
        }
        return response


api.add_resource(CrossLocationsLinksData, '/crossLocationLinks/<int:polygon_id>')
api.add_resource(POILocationsLinksData, '/poiLinks/<int:polygon_id>')