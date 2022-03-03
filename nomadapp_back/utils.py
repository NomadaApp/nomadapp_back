import geopy.distance
import logging

logger = logging.getLogger().getChild(__name__)


def distance_from_location(coord, location):
    try:
        distance = geopy.distance.great_circle(coord, location).km
        return distance
    except ValueError:
        logger.warning('Error calculating distances between two locations')


def create_distance_column(query, coordinates):
    query['coord'] = list(zip(query.lat, query.lon))
    return list(map(lambda coord: distance_from_location(coord, coordinates.values()), query.coord))
