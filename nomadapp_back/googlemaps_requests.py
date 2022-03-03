import pandas as pd
from nomadapp_back.Class_definitions import Education, Restaurants, Leisure, Coworking
import googlemaps


API_KEY = "AIzaSyCMxtTJa-B0ojhq7zsyw84g0TvncgEU7Yc"


def gm_client(key: str):
    try:
        return googlemaps.Client(key=key)
    except ValueError as e:
        print(e)


def get_coordinates(location: str, gmaps_obj):
    coordinates = gmaps_obj.geocode(location)
    # Middle of the district
    point = coordinates[0]["geometry"].get("location")
    return point


def query_execution(
    selection: list, point: dict, radius: int, gmaps: googlemaps.client.Client
):

    final_data = pd.DataFrame()

    if "education" in selection:
        education = Education(point, radius, gmaps)
        e_request = education.api_request()
        ed_table = education.json_to_table(e_request)
        ed_table["Type"] = "education"
        final_data = pd.concat([final_data, ed_table])

    if "coworking" in selection:
        coworking = Coworking(point, radius, gmaps)
        c_request = coworking.api_request()
        co_table = coworking.json_to_table(c_request)
        co_table["Type"] = "coworking"
        final_data = pd.concat([final_data, co_table])

    if "restaurants" in selection:
        food_drinks = Restaurants(point, radius, gmaps)
        f_request = food_drinks.api_request()
        food_table = food_drinks.json_to_table(f_request)
        food_table["Type"] = "restaurants"
        final_data = pd.concat([final_data, food_table])

    if "leisure" in selection:
        leisure = Leisure(point, radius, gmaps)
        l_request = leisure.api_request()
        le_table = leisure.json_to_table(l_request)
        le_table["Type"] = "leisure"
        final_data = pd.concat([final_data, le_table])

    return final_data
