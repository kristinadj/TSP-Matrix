from flask import request
from flask_restx import Resource

from ..util.dto import LocationDTO
from ..service.location_service import add_locations

api = LocationDTO.api
_location = LocationDTO.location

@api.route('')
class LocationsCollection(Resource):

    @api.expect([_location], validate=True)
    @api.response(201, 'Locations successfully added')
    @api.doc('adding new locations')
    def post(self):
        """Adding new locations"""
        data = request.json
        return add_locations(data=data)