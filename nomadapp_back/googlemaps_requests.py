import pandas as pd
import googlemaps
import logging
from nomadapp_back.Class_definitions import Education, Restaurants, Leisure, Coworking

# Calling the logger to this file
logger = logging.getLogger().getChild(__name__)

# Google Maps API key
API_KEY = "AIzaSyCMxtTJa-B0ojhq7zsyw84g0TvncgEU7Yc"


def get_coordinates(location: str, gmaps_obj: googlemaps.client.Client):
    """
    Apply the Google Maps function 'geocode' to the location string.
    From the results, extracts the coordinates of the place.

    Params:
        -location: string -> It could be a city, an address, a postal code... given by the user
        -gmaps_obj: Google Maps client object. For geocode function usage
    Returns:
        Dictionary with latitude and longitude extracted from the json provided by the geocode function
        If the json is empty, it means than the coordinates has not been founded, and it will raise an error
    """
    try:
        coordinates = gmaps_obj.geocode(location)
        return coordinates[0]["geometry"].get("location")
    except IndexError:
        raise IndexError


def query_execution(selection: list, point: dict, radius: int, gmaps: googlemaps.client.Client):
    """
    This function checks in the selection list the filters than the user has chosen.

    When a filter is founded in the list:
        1. Creates the specific filter class
        2. Calls the class abstract method 'api_request' to make the query to the Google Maps API
        3. Calls the class method 'json_to_table' to convert the results to a dataframe
        4. Adds the name of the filter to a new column in the dataframe
        5. Appends the results to the final dataframe

    Params:
        -selection: list of place types that the user wants to search
        -point: dict with longitude and latitude where the request will be done
        -radius: int. The results of the Google Maps API request will be filtered by this limit
        -gmaps: Google Maps client object. For geocode function usage

    Returns:
        Dataframe with the results of the different filters appended
    """

    # Creation of the dataframe where the results will be appended
    final_results = pd.DataFrame()

    # Filters verification. When a filter is founded in the selection list, the previous described steps are applied
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

    # Final dataframe with all the results
    return final_results

