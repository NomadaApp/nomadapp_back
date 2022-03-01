from utils import query_execution, get_coordinates
import googlemaps

params = {
    "selection": [
        "Food_and_Drinks", "Education"],
    "location": "Barrio Salamanca",
    "radius": 2000
}

API_KEY = 'AIzaSyCMxtTJa-B0ojhq7zsyw84g0TvncgEU7Yc'


def gm_client(key: str):
    try:
        return googlemaps.Client(key=key)
    except ValueError as e:
        print(e)


if __name__ == "__main__":

    # Instantiate the Google.client class
    gmaps = gm_client(API_KEY)

    # Get the coordinates selected by the user
    coordinates = get_coordinates(params.get('location'), gmaps)

    # Get the radius selected by the user
    radius = params.get('radius')

    # Execute query through function
    results_dataframe = query_execution(params.get('selection'), coordinates, radius, gmaps)

    # Save the table with the results from the query
    results_dataframe.to_csv('data.csv', index=False)
