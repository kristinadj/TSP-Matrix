from .. import db

from geoalchemy2 import Geometry


class Location(db.Model):
    """A location, including its geospatial data"""

    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    polygon_id = db.Column(db.Integer, db.ForeignKey('polygons.id'), nullable=False,)
    is_cross_location = db.Column(db.Boolean, nullable=False, default=False)
    geo = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

    def __repr__(self):
        return '<Location {name}, ({lat}, {lon})>'.format(name=self.location_name, lat=self.latitude, lon=self.longitude)