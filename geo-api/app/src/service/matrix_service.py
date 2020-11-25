from app.src import db

from app.src.model.polygon import Polygon
from app.src.model.location import Location
from app.src.model.matrix_row import MatrixRow

from sqlalchemy import func
from sqlalchemy.orm import aliased, joinedload
from geoalchemy2 import functions
import requests
import sys



def get_cross_locations_data():
    response = []
    from_location, to_location = aliased(Location), aliased(Location)

    cross_locations_data = MatrixRow.query \
                                     .join(from_location, MatrixRow.from_location_id == from_location.id) \
                                     .join(to_location, MatrixRow.to_location_id == to_location.id) \
                                     .with_entities(from_location.polygon_id, to_location.polygon_id, MatrixRow.from_location_id, MatrixRow.to_location_id, MatrixRow.distance, MatrixRow.duration) \
                                     .filter(from_location.is_cross_location & \
                                             to_location.is_cross_location & \
                                            (from_location.polygon_id != to_location.polygon_id)) \
                                     .all()

    for item in cross_locations_data:
        cross_location_link = {
            'fromPolygon': item[0],
            'toPolygon': item[1],
            'fromLocation': item[2],
            'toLocation': item[3],
            'distance': item[4],
            'duration': item[5]
        }
        response.append(cross_location_link)
    
    return response


def get_cross_locations_data_csv():
    result = []
    from_location, to_location = aliased(Location), aliased(Location)

    cross_locations_data = MatrixRow.query \
                                     .join(from_location, MatrixRow.from_location_id == from_location.id) \
                                     .join(to_location, MatrixRow.to_location_id == to_location.id) \
                                     .with_entities(from_location.latitude, from_location.longitude, from_location.name, \
                                                    to_location.latitude, to_location.longitude, to_location.name) \
                                     .filter(from_location.is_cross_location & \
                                             to_location.is_cross_location & \
                                            (from_location.polygon_id != to_location.polygon_id)) \
                                     .all()

    for item in cross_locations_data:   
        opposit_link = [item[3], item[4], item[5], True, item[0], item[1], item[2], True]
        if opposit_link not in result:
            cross_location_link = [item[0], item[1], item[2], True, item[3], item[4], item[5], True]
            result.append(cross_location_link)

    return result


def get_cross_locations_links_data(polygon_id):
    response = []
    from_location, to_location = aliased(Location), aliased(Location)

    cross_location_links_data = MatrixRow.query \
                                         .join(from_location, MatrixRow.from_location_id == from_location.id) \
                                         .join(to_location, MatrixRow.to_location_id == to_location.id) \
                                         .with_entities(MatrixRow.from_location_id, MatrixRow.to_location_id, MatrixRow.distance, MatrixRow.duration) \
                                         .filter(from_location.is_cross_location & \
                                                 to_location.is_cross_location & \
                                                (from_location.polygon_id == polygon_id) &
                                                (to_location.polygon_id == polygon_id)) \
                                         .all()

    for item in cross_location_links_data:
        cross_location_link = {
            'fromLocation': item[0],
            'toLocation': item[1],
            'distance': item[2],
            'duration': item[3]
        }
        response.append(cross_location_link)

    return response


def get_poi_links_data(polygon_id):
    response = []
    from_location, to_location = aliased(Location), aliased(Location)

    poi_links_data = MatrixRow.query \
                              .join(from_location, MatrixRow.from_location_id == from_location.id) \
                              .join(to_location, MatrixRow.to_location_id == to_location.id) \
                              .with_entities(MatrixRow.from_location_id, MatrixRow.to_location_id, MatrixRow.distance, MatrixRow.duration) \
                              .filter( \
                                  (from_location.polygon_id == polygon_id) & \
                                  (to_location.polygon_id == polygon_id) & \
                                  # poi - poi
                                  (~from_location.is_cross_location) & \
                                  (~to_location.is_cross_location)
                              ) \
                              .all()

    for item in poi_links_data:
        poi_link = {
            'fromLocation': item[0],
            'toLocation': item[1],
            'distance': item[2],
            'duration': item[3]
        }
        response.append(poi_link)

    return response


def get_location_links_data(polygon_id):
    response = []
    from_location, to_location = aliased(Location), aliased(Location)

    poi_links_data = MatrixRow.query \
                              .join(from_location, MatrixRow.from_location_id == from_location.id) \
                              .join(to_location, MatrixRow.to_location_id == to_location.id) \
                              .with_entities(MatrixRow.from_location_id, MatrixRow.to_location_id, MatrixRow.distance, MatrixRow.duration) \
                              .filter( \
                                  (from_location.polygon_id == polygon_id) & \
                                  (to_location.polygon_id == polygon_id)) \
                              .filter(
                                  # cross location - poi
                                  (from_location.is_cross_location & ~to_location.is_cross_location) | \
                                  # poi - cross location
                                  (~from_location.is_cross_location & to_location.is_cross_location) | \
                                  # cross location - cross - location
                                  (from_location.is_cross_location & to_location.is_cross_location) \
                              ) \
                              .all()

    for item in poi_links_data:
        poi_link = {
            'fromLocation': item[0],
            'toLocation': item[1],
            'distance': item[2],
            'duration': item[3]
        }
        response.append(poi_link)

    return response

def get_location_links_data_csv(polygon_id):
    result = []
    from_location, to_location = aliased(Location), aliased(Location)

    poi_links_data = MatrixRow.query \
                              .join(from_location, MatrixRow.from_location_id == from_location.id) \
                              .join(to_location, MatrixRow.to_location_id == to_location.id) \
                              .with_entities(from_location.latitude, from_location.longitude, from_location.name, from_location.is_cross_location, \
                                             to_location.latitude, to_location.longitude, to_location.name, to_location.is_cross_location) \
                              .filter( \
                                  (from_location.polygon_id == polygon_id) & \
                                  (to_location.polygon_id == polygon_id)) \
                              .filter(
                                  # cross location - poi
                                  (from_location.is_cross_location & ~to_location.is_cross_location) | \
                                  # poi - cross location
                                  (~from_location.is_cross_location & to_location.is_cross_location) | \
                                  # cross location - cross - location
                                  (from_location.is_cross_location & to_location.is_cross_location) \
                              ) \
                              .all()

    for item in poi_links_data:
        opposit_link = [item[4], item[5], item[6], item[7],item[0], item[1], item[2], item[3]]
        if opposit_link not in result:
            cross_location_link = [item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]]
            result.append(cross_location_link)

    return result


def generate_for_all_polygons():
    polygons = Polygon.query.all()

    for polygon in polygons:
        print(polygon.id)
        locations = Location.query.filter(Location.polygon_id == polygon.id).all()

        if len(locations) == 1:
            continue

        osrm_table = _get_osrm_table_response(locations)

        if not osrm_table:
            return False
        
        for i in range(len(locations)):
            for j in range(i+1, len(locations)):
                # direction i -> j
                row = MatrixRow.query.filter((MatrixRow.from_location_id == locations[i].id) & (MatrixRow.to_location_id == locations[j].id)).first()

                if not row:
                    row = MatrixRow(
                        from_location_id=locations[i].id,
                        to_location_id=locations[j].id,
                        distance = osrm_table['distances'][i][j],
                        duration =  osrm_table['durations'][i][j]
                    )
                    db.session.add(row)

                # direction j -> i
                row = MatrixRow.query.filter((MatrixRow.from_location_id == locations[j].id) & (MatrixRow.to_location_id == locations[i].id)).first()

                if not row:
                    row = MatrixRow(
                        from_location_id=locations[j].id,
                        to_location_id=locations[i].id,
                        distance = osrm_table['distances'][j][i],
                        duration = osrm_table['durations'][j][i]
                    )
                    db.session.add(row)
        db.session.commit()

    return True


def generate_for_neighbour_polygons():
    polygons = Polygon.query.all()

    for polygon in polygons:
        print(polygon.id)
        neighbours = db.session.query(Polygon).filter((Polygon.id != polygon.id) & (func.ST_Intersects(Polygon.geo, polygon.geo))).all()
        neighbours_ids = [x.id for x in neighbours if 'POINT' not in db.session.scalar(functions.ST_AsText(functions.ST_Intersection(polygon.geo, x.geo)))]

        polygon_cross_locations = Location.query.filter((Location.polygon_id == polygon.id) & (Location.is_cross_location == True)).all()
        neighbours_cross_locations = Location.query.filter((Location.polygon_id.in_(neighbours_ids)) & (Location.is_cross_location == True)).all()

        if len(polygon_cross_locations) + len(neighbours_cross_locations) == 1:
            continue

        size = len(polygon_cross_locations) + len(neighbours_cross_locations)
        osrm_table = _get_osrm_table_response_s2d(polygon_cross_locations, neighbours_cross_locations)

        if not osrm_table:
            return False

        for i in range(len(polygon_cross_locations)):
            nearest_idx = _find_nearest(i, osrm_table)
            row = MatrixRow.query.filter((MatrixRow.from_location_id == polygon_cross_locations[i].id) & (MatrixRow.to_location_id == neighbours_cross_locations[nearest_idx].id)).first()

            if not row:
                row = MatrixRow(
                    from_location_id=polygon_cross_locations[i].id,
                    to_location_id=neighbours_cross_locations[nearest_idx].id,
                    distance = osrm_table['distances'][i][nearest_idx],
                    duration =  osrm_table['durations'][i][nearest_idx]
                )
                db.session.add(row)
        db.session.commit()
    
    return True


def _get_osrm_table_response(locations):
    url = 'http://router.project-osrm.org/table/v1/driving/@COORDS@?annotations=duration,distance'
    str_coords = ['{:.6f},{:.6f}'.format(i.longitude, i.latitude) for i in locations]
    url = url.replace('@COORDS@', ';'.join(str_coords))

    osrm_response = requests.get(url)
    
    if osrm_response.status_code == 200:
        return osrm_response.json()
    
    return None


def _get_osrm_table_response_s2d(source_locations, destination_locations):
    url = 'http://router.project-osrm.org/table/v1/driving/@COORDS@?sources=@S_INDEX@&destinations=@D_INDEX@&annotations=duration,distance'
    url = url.replace('@S_INDEX@', ';'.join(str(x) for x in range(0, len(source_locations))))
    url = url.replace('@D_INDEX@', ';'.join(str(x) for x in range(len(source_locations), len(destination_locations) + len(source_locations))))

    locations = source_locations + destination_locations
    str_coords = ['{:.6f},{:.6f}'.format(i.longitude, i.latitude) for i in locations]
    url = url.replace('@COORDS@', ';'.join(str_coords))
    #print(url)
    osrm_response = requests.get(url)
    
    if osrm_response.status_code == 200:
        return osrm_response.json()
    
    return None


def _find_nearest(idx, osrm_table):
    min_distance = sys.maxsize
    nearest_idx = None

    for j in range(len(osrm_table['distances'][idx])):
        distance = osrm_table['distances'][idx][j]
        if distance < min_distance:
            min_distance = distance
            nearest_idx = j
    
    return nearest_idx