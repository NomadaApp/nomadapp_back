from flask import Flask, jsonify, request
import os
import googlemaps
import logging.config
import logging
from nomadapp_back.googlemaps_requests import (
    API_KEY,
    query_execution,
    get_coordinates
)

# Creating a logger with the configuration detailed in 'logging.conf'
logging.config.fileConfig('logger/logging.conf')
logger = logging.getLogger(__name__)


'''
Creating an instance of the Flask object. 
This API will be communicated with the front (Streamlit) and the Google Maps API.
It will receive the params selected by the user to make the request to Google Maps API, and will send the cleaned
results back to the front, in order to display them in an interactive map.
'''
app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    return "Hello World"


@app.route("/json-request", methods=["GET"])
def get_params():
    # 1. Receives from the front the dictionary with the user requested params to make the query
    query = request.args

    # 2. Creation the Google Maps client object. If fails, returns a message to the front
    try:
        gmaps = googlemaps.Client(key=API_KEY)
    except ValueError:
        logging.warning('Invalid API KEY')
        return jsonify({'Error': 'Invalid API KEY'})

    # 3. Extraction of the places that the user wants, and the radius in which the query will be based on
    selection = [key for key, item in query.items() if item == "True"]
    radius = int(query.get("radius"))

    # 4. Conversion of the given location (in string format) to coordinates. If fails, returns a message to the front
    try:
        location = get_coordinates(query.get("location"), gmaps)
    except IndexError:
        logging.warning('Incorrect location input')
        return jsonify({'Error': 'Incorrect location input'})

    # 5. Obtaining the dataframe through the 'query_execution' function, which makes the query with the selected params
    # and returns a dataframe.
    query_dataframe = query_execution(selection, location, radius, gmaps)

    # 6. If the dataframe is empty sends a 'Not results founded' message. If not, reset the index to avoid problems
    # with the jsonify function, and sends the final results to the front
    if query_dataframe.empty is False:
        query_dataframe.reset_index(drop=True, inplace=True)
        results = query_dataframe.to_json()
        logging.info('Results founded!')
        return jsonify(results)
    else:
        logging.warning('Not results founded')
        return jsonify({'Error': 'Not results founded'})


if __name__ == "__main__":
    # Run the Flask API
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
