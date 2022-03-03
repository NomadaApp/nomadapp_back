from abc import ABC, abstractmethod
import pandas as pd
from nomadapp_back.utils import create_distance_column
import logging

logger = logging.getLogger().getChild(__name__)


class Filters(ABC):

    def __init__(self, location, radius, gmaps):
        self.location = location
        self.radius = radius
        self.gmaps = gmaps

    @abstractmethod
    def api_request(self):
        pass

    def json_to_table(self, query_json):
        query_df = pd.DataFrame()

        query_df['Name'] = pd.Series(map(lambda name: name['name'],
                                         query_json['results']))
        query_df['lat'] = pd.Series(map(lambda lat: lat['geometry'].get('location').get('lat'),
                                        query_json['results']))
        query_df['lon'] = pd.Series(map(lambda long: long['geometry'].get('location').get('lng'),
                                        query_json['results']))
        query_df['distance_from_location'] = create_distance_column(query_df, self.location)
        query_df['rating'] = pd.Series(map(lambda status: status['rating'],
                                           query_json['results']))

        query_df_filtered = query_df[query_df['distance_from_location'] <= self.radius]

        return query_df_filtered


class Coworking(Filters):
    def api_request(self):
        query_json = self.gmaps.places('coworking', location=self.location, radius=self.radius)
        logging.info('Searching coworking places')
        return query_json


class Education(Filters):
    def api_request(self):
        query_json = self.gmaps.places(location=self.location, type='secondary_school', radius=self.radius)
        logging.info('Searching education places')
        return query_json


class Restaurants(Filters):
    def api_request(self):
        restaurants_request = self.gmaps.places(location=self.location, type='restaurant', radius=self.radius)
        logging.info('Searching restaurants')
        return restaurants_request


class Leisure(Filters):
    def api_request(self):
        leisure_request = self.gmaps.places(location=self.location, type='night_club', radius=self.radius)
        logging.info('Searching leisure places')
        return leisure_request
