from .. import db

from geoalchemy2 import Geography


class Polygon(db.Model):
    """A polygon, including its geospatial data."""

    __tablename__ = 'polygons'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    geo = db.Column(Geography(geometry_type='POLYGON', srid=4326, spatial_index=True), nullable=False)

    def __repr__(self):
        return '<Polygon {name}>'.format( name=self.polygon_name)