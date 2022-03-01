import pandas as pd
from Class_definitions import Education, FoodAndDrinks, Coworking
import googlemaps


def get_coordinates(location: str, gmaps_obj):
    coordinates = gmaps_obj.geocode(location)
    # Middle of the district
    point = coordinates[0]['geometry'].get('location')
    return point


def query_execution(selection: list, point: dict, radius: int, gmaps: googlemaps.client.Client):

    final_data = pd.DataFrame()

    if 'Education' in selection:
        education = Education(point, radius, gmaps)
        e_request = education.api_request()
        ed_table = education.json_to_table(e_request)
        ed_table['Type'] = 'Education'
        final_data = pd.concat([final_data, ed_table])

    if 'Coworking' in selection:
        coworking = Coworking(point, radius, gmaps)
        c_request = coworking.api_request()
        co_table = coworking.json_to_table(c_request)
        co_table['Type'] = 'Coworking'
        final_data = pd.concat([final_data, co_table])

    if 'Food and Drinks' in selection:
        food_drinks = FoodAndDrinks(point, radius, gmaps)
        f_request = food_drinks.api_request()
        food_table = food_drinks.json_to_table(f_request)
        food_table['Type'] = 'Food and Drinks'
        final_data = pd.concat([final_data, food_table])

    return final_data
