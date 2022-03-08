import geopy.distance
import logging

# Calling the logger to this file
logger = logging.getLogger().getChild(__name__)


def distance_from_location(coord: tuple, location: tuple):
    """
    Calculates the distance between two points through the geopy.distance module
    Params:
        - coord: tuple with the coordinates of the first point
        - location: tuple with the coordinates of the second point
    Returns:
        Float with the distance between the two points, expressed in kilometers.
        If fails, a logger warning will be written.
    """
    try:
        distance = geopy.distance.great_circle(coord, location).km
        return distance
    except ValueError:
        logger.warning("Error calculating distances between two locations")


def create_distance_column(query, coordinates: dict):
    """
    Receives a dataframe. Creates a new column where joins the latitude and longitude into one column, and
    apply to that new column the distance_from_location function to return a new list.
    Params:
        - query: dataframe with the query results
        - coordinates: dict with longitude and latitude where the request has been done
    Returns:
        List with the distances between each coordinate of the daframe column 'coord' and the givben coordinates
    """
    query["coord"] = list(zip(query.lat, query.lon))
    return list(
        map(
            lambda coord: distance_from_location(coord, coordinates.values()),
            query.coord,
        )
    )
