from app.src import db
from app.src.model.location import Location
from app.src.model.polygon import Polygon

from sqlalchemy import func

def add_locations(data):
    for l in data:

        location = Location.query.filter_by(name=l['name']).first()

        if not location:
            point_geo_str = 'POINT({:s})'.format('{:.6f}'.format(l['lon']) + ' ' + '{:.6f}'.format(l['lat']))
            polygon = db.session.query(Polygon).filter(func.ST_Intersects(point_geo_str, Polygon.geo)).first()

            if not polygon:
                response = {
                    'status': 'fail',
                    'message': 'Location ' + l['name'] + ' does not belong to any polygon'
                }
                return response, 400


            new_location = Location(
                name=l['name'],
                latitude=l['lat'],
                longitude=l['lon'],
                geo=point_geo_str,
                polygon_id=polygon.id,
                is_cross_location=l['is_cross_location']
            )
            save(new_location)

        else:
            response = {
                'status': 'fail',
                'message': 'Location ' + l['name'] + ' name already exists'
            }
            return response, 400
    
    response = {
        'status': 'success',
        'message': 'Locations successfully added'
    }
    return response, 201


def get_poi_ids(polygon_id):
    pois = Location.query.filter((Location.polygon_id == polygon_id) & (~Location.is_cross_location)).all()
    return [poi.id for poi in pois]


def save(data):
    db.session.add(data)
    db.session.commit()