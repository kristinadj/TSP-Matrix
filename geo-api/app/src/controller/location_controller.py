from flask import request, make_response
from flask_restx import Resource
import io, csv

from ..util.dto import LocationDTO
from ..service.location_service import add_locations, get_pois_csv_format

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

    
    @api.doc('Get csv file with POIs info')
    def get(self):
        """Get csv file with POIs info"""
        pois = get_pois_csv_format()
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerows(pois)
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output