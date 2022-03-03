import pandas as pd
from nomadapp_back.Class_definitions import Education, Restaurants, Leisure, Coworking
import googlemaps


API_KEY = 'AIzaSyCMxtTJa-B0ojhq7zsyw84g0TvncgEU7Yc'


def gm_client(key: str):
    try:
        return googlemaps.Client(key=key)
    except ValueError as e:
        print(e)


def get_coordinates(location: str, gmaps_obj):
    coordinates = gmaps_obj.geocode(location)
    # Middle of the district
    try:
        point = coordinates[0]['geometry'].get('location')
        return point
    except IndexError:
        return []
gmaps = gm_client(API_KEY)
get_coordinates('Madrid', gmaps)
def query_execution(selection: list, point: dict, radius: int, gmaps: googlemaps.client.Client):

    final_data = pd.DataFrame()

    if 'education' in selection:
        education = Education(point, radius, gmaps)
        e_request = education.api_request()
        e_table = education.json_to_table(e_request)
        e_table['Type'] = 'education'
        final_data = pd.concat([final_data, e_table])

    if 'coworking' in selection:
        coworking = Coworking(point, radius, gmaps)
        c_request = coworking.api_request()
        c_table = coworking.json_to_table(c_request)
        c_table['Type'] = 'coworking'
        final_data = pd.concat([final_data, c_table])

    if 'restaurants' in selection:
        restaurants = Restaurants(point, radius, gmaps)
        r_request = restaurants.api_request()
        r_table = restaurants.json_to_table(r_request)
        r_table['Type'] = 'restaurants'
        final_data = pd.concat([final_data, r_table])

    if 'leisure' in selection:
        leisure = Leisure(point, radius, gmaps)
        l_request = leisure.api_request()
        l_table = leisure.json_to_table(l_request)
        l_table['Type'] = 'leisure'
        final_data = pd.concat([final_data, l_table])

    return final_data

