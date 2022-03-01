import googlemaps
import pandas as pd
from Class_definitions import Coworking, Education, Food_and_Drinks

df = pd.read_csv('../data.csv')
API_KEY = 'AIzaSyCMxtTJa-B0ojºhq7zsyw84g0TvncgEU7Yc'

try:
    gmaps = googlemaps.Client(key=API_KEY)

except ValueError as e:
    print(e)

def query_execution(final_selection : dict):

    final_data = pd.DataFrame()

    if 'Education' in final_selection.keys():
        education = Education(point, radius, gmaps)
        e_request = education.api_request()
        ed_table = education.json_to_table(e_request)
        ed_table['Type'] = 'Education'
        final_data = pd.concat([final_data, ed_table])

    if 'Coworking' in final_selection.keys():
        coworking = Coworking(point, radius, gmaps)
        c_request = coworking.api_request()
        co_table = coworking.json_to_table(c_request)
        co_table['Type'] = 'Coworking'
        final_data = pd.concat([final_data, co_table])

    if 'Food_and_Drinks' in final_selection.keys():
        food_drinks = Food_and_Drinks(point, radius, gmaps)
        f_request = food_drinks.api_request()
        food_table = food_drinks.json_to_table(f_request)
        food_table['Type'] = 'Food and Drinks'
        final_data = pd.concat([final_data, food_table])

    return final_data

if __name__ == "__main__":

    '''
    GETTING COORDINATES FROM STRING
    '''

    coordinates = gmaps.geocode('Barrio Salamanca, Madrid')
    # Middle of the district
    point = coordinates[0]['geometry'].get('location')
    radius = 2000

    '''GETTING FILTER OBJECTS FROM DICTIONARY'''

    dict_params = {'Coworking': True, 'Education': False, 'Food_and_Drinks': True, 'Leisure': False}
    final_selection = dict(filter(lambda x: x[1] is True, dict_params.items()))

    final_table = query_execution(final_selection)
    final_table.to_csv('data.csv', index = False)


