from abc import ABC, abstractmethod
import pandas as pd
from nomadapp_back.utils import create_distance_column
import logging

# Calling the logger to this file
logger = logging.getLogger().getChild(__name__)


class Filters(ABC):
    """
    Abstract class that will be inherited by the child classes (different type of filters).
    It has to receive 3 params and has two methods:
        -abstract method to implement the api request for each kind of filter
        -method that converts to a Dataframe and filters the results of any subclass request to the API
    """

    def __init__(self, location, radius, gmaps):
        """
        Params:
            -Location: dict with longitude and latitude where the request will be done
            -radius: int. The results of the Google Maps API request will be filtered by this limit
            -gmaps: Google Maps client object. For places function usage
        """
        self.location = location
        self.radius = radius
        self.gmaps = gmaps

    @abstractmethod
    def api_request(self):
        """
        This method will be implemented by each child class, with the specific Google Maps Api query
        Returns:
            -Json with the results of the query
        """
        pass

    def json_to_table(self, query_json):
        """
        Converts a raw json with all the data from the query to a filtered dataframe with the results we want
        to send back to the user.
        Param :
            -query_json: json file with the raw data extracted from the Google Maps API query
        Return:
            -Dataframe with the desirable info: Name, location, distance from main point and rating
             of each place founded in the results. It will be filtered with the places whose distance from the main
             location is less than the radius selected
        """
        # 1. Create the dataframe
        query_df = pd.DataFrame()

        # 2. Extract the info we want to send to the front
        query_df['Name'] = pd.Series(map(lambda name: name['name'],
                                         query_json['results']))
        query_df['lat'] = pd.Series(map(lambda lat: lat['geometry'].get('location').get('lat'),
                                        query_json['results']))
        query_df['lon'] = pd.Series(map(lambda long: long['geometry'].get('location').get('lng'),
                                        query_json['results']))
        # Creates a new column calculating the distance from each place to the given location
        query_df['distance_from_location'] = create_distance_column(query_df, self.location)
        query_df['rating'] = pd.Series(map(lambda status: status['rating'],
                                           query_json['results']))

        # 3. Filter the results according to the given radius
        query_df_filtered = query_df[query_df['distance_from_location'] <= self.radius]

        # 4. Return the filtered dataframe
        return query_df_filtered


# Coworking filter
class Coworking(Filters):
    def api_request(self):
        query_json = self.gmaps.places('coworking', location=self.location, radius=self.radius)
        logging.info('Searching coworking places')
        return query_json


# Education filter
class Education(Filters):
    def api_request(self):
        query_json = self.gmaps.places(location=self.location, type='secondary_school', radius=self.radius)
        logging.info('Searching education places')
        return query_json


# Restaurant filter
class Restaurants(Filters):
    def api_request(self):
        restaurants_request = self.gmaps.places(location=self.location, type='restaurant', radius=self.radius)
        logging.info('Searching restaurants')
        return restaurants_request


# Leisure filter
class Leisure(Filters):
    def api_request(self):
        leisure_request = self.gmaps.places(location=self.location, type='night_club', radius=self.radius)
        logging.info('Searching leisure places')
        return leisure_request
