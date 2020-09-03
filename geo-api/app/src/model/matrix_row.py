from .. import db

class MatrixRow(db.Model):
    """Row in matrix."""

    __tablename__ = 'locations_matrix'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    to_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    distance = db.Column(db.Float)
    duration = db.Column(db.Float)

    def __repr__(self):
        return '<MatrixRow {from_loc} - {to_loc}: distance {dist}; duration {duration}>'.format( 
            from_loc=self.from_location_id, to_loc=self.to_location_id, distance=self.distance, duration=self.duration
            )