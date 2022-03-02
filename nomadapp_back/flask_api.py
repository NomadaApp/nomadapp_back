from flask import Flask, jsonify, request
from googlemaps_requests import gm_client, API_KEY, query_execution, get_coordinates
import os



app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    return "Hello World"


@app.route("/json-request", methods=["GET"])
def get_params():
    query = request.args

    gmaps = gm_client(API_KEY)

    selection = [key for key, item in query.items() if item == "True"]
    radius = query.get("radius")
    location = get_coordinates(query.get("location"), gmaps)

    query_dataframe = query_execution(selection, location, radius, gmaps)
    results = query_dataframe.to_json()
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
