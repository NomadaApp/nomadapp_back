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


app = Flask(__name__)

logging.config.fileConfig('logger/logging.conf')
logger = logging.getLogger(__name__)


@app.route("/", methods=["GET"])
def hello():
    return "Hello World"


@app.route("/json-request", methods=["GET"])
def get_params():

    query = request.args

    try:
        gmaps = googlemaps.Client(key=API_KEY)
    except ValueError:
        logging.warning('Invalid API KEY')
        return jsonify({'Error': 'Invalid API KEY'})

    selection = [key for key, item in query.items() if item == "True"]
    radius = int(query.get("radius"))
    try:
        location = get_coordinates(query.get("location"), gmaps)
    except IndexError:
        logging.warning('Incorrect location input')
        return jsonify({'Error': 'Incorrect location input'})
    query_dataframe = query_execution(selection, location, radius, gmaps)

    if query_dataframe.empty is False:
        query_dataframe.reset_index(drop=True, inplace=True)
        results = query_dataframe.to_json()
        logging.info('Results founded!')
        return jsonify(results)
    else:
        logging.warning('Not results founded')
        return jsonify({'Error': 'Not results founded'})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
