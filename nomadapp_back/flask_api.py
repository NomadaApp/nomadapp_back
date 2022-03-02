from flask import Flask, jsonify, request
import os
import sqlite3
import requests

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    return "Hello World"


@app.route("/json-request", methods=["GET"])
def get_params():
    # query = request.get_json()
    query = request.args

    # selection = [key for key, item in query.items() if item == "True"]
    selection = []
    radius = query.get("radius")
    location = query.get("location")

    results = {
        "Recibido Antonio": True,
        "selection": selection,
        "radius": radius,
        "location": location,
    }
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
