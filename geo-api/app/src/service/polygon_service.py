from app.src import db
from app.src.model.polygon import Polygon


def add_polygon(data):
    polygon = Polygon.query.filter_by(name=data['name']).first()

    if not polygon:
        new_polygon = Polygon(
            name=data['name'],
            geo=data['geo']
        )
        save(new_polygon)

        response = {
            'status': 'success',
            'message': 'Polygon successfully created'
        }
        return response, 201
    else:
        response = {
            'status': 'fail',
            'message': 'Polygon name already exists'
        }
        return response, 400

def get_all():
    return Polygon.query.all()

def get_by_id(polygon_id):
    return Polygon.query.filter_by(id=polygon_id).first()

def save(data):
    db.session.add(data)
    db.session.commit()