import geopy.distance


def distance_from_location(coord, location):
    return (geopy.distance.great_circle(coord, location).km)


def create_distance_column(query, coordinates):
    query['coord'] = list(zip(query.lat, query.lon))
    return list(map(lambda coord: distance_from_location(coord, coordinates.values()), query.coord))