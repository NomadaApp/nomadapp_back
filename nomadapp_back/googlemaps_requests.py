import pandas as pd
from nomadapp_back.Class_definitions import Education, Restaurants, Leisure, Coworking
import googlemaps
import logging

logger = logging.getLogger().getChild(__name__)

API_KEY = "AIzaSyCMxtTJa-B0ojhq7zsyw84g0TvncgEU7Yc"


def get_coordinates(location: str, gmaps_obj):
    try:
        coordinates = gmaps_obj.geocode(location)
        return coordinates[0]["geometry"].get("location")
    except IndexError:
        raise IndexError


def query_execution(selection: list, point: dict, radius: int, gmaps: googlemaps.client.Client):

    final_results = pd.DataFrame()

    if "education" in selection:
        education = Education(point, radius, gmaps)
        e_request = education.api_request()

        education_df = education.json_to_table(e_request)
        education_df["Type"] = "education"
        final_results = pd.concat([final_results, education_df])

    if "coworking" in selection:
        coworking = Coworking(point, radius, gmaps)
        c_request = coworking.api_request()

        coworking_df = coworking.json_to_table(c_request)
        coworking_df["Type"] = "coworking"
        final_results = pd.concat([final_results, coworking_df])

    if "restaurants" in selection:
        restaurants = Restaurants(point, radius, gmaps)
        r_request = restaurants.api_request()

        restaurants_df = restaurants.json_to_table(r_request)
        restaurants_df["Type"] = "restaurants"
        final_results = pd.concat([final_results, restaurants_df])

    if "leisure" in selection:
        leisure = Leisure(point, radius, gmaps)
        l_request = leisure.api_request()

        leisure_df = leisure.json_to_table(l_request)
        leisure_df["Type"] = "leisure"
        final_results = pd.concat([final_results, leisure_df])

    return final_results

