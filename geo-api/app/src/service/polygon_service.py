from app.src import db
from app.src.model.polygon import Polygon

from geoalchemy2 import WKBElement
from sqlalchemy import func

import functools
import operator


def add_polygons(data):
    for p in data:
        polygon = Polygon.query.filter_by(name=p['name']).first()

        if not polygon:
            flatten_coords_list = functools.reduce(operator.iconcat, p['coordinates'], [])
            flatten_coords_list_str = ['{:.6f}'.format(i) for i in flatten_coords_list]
            coords_pairs_list = [' '.join(i) for i in zip(flatten_coords_list_str[::2], flatten_coords_list_str[1::2])]

            new_polygon = Polygon(
                name=p['name'],
                geo='POLYGON(({:s}))'.format(', '.join(coords_pairs_list))
            )
            save(new_polygon)
        else:
            response = {
                'status': 'fail',
                'message': 'Polygon name ' +  p['name'] + ' already exists'
            }
            return response, 400
    
    response = {
        'status': 'success',
        'message': 'Polygons successfully added'
    }
    return response, 201


def get_all():
    response = []
    polygons = Polygon.query.all()

    for p in polygons:
        neighbours_ids = [x.id for x in polygons if x.id != p.id  and db.session.scalar(p.geo.ST_Intersects(x.geo))] 

        polygon = {
            'id' : p.id,
            'neighbours_ids' : neighbours_ids
        }
        response.append(polygon)

    return response


def get_by_id(polygon_id):
    return Polygon.query.filter_by(id=polygon_id).first()


def save(data):
    db.session.add(data)
    db.session.commit()