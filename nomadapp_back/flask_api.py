from flask import Flask, jsonify, request
import sqlite3
import requests

app = Flask(__name__)

root_path = "http://127.0.0.1:5000"


@app.route("/", methods=["GET"])
def hello():
    return "Hello World"


@app.route("/json-request", methods=["GET"])
def get_params():
    query = request.get_json()

    selection = [key for key, item in query.items() if item == "True"]
    radius = query.get("radius")
    location = query.get("location")

    results = {
        "Recibido Antonio": True,
        "selection": selection,
        "radius": radius,
        "location": location,
    }
    return jsonify(results)


app.run(host="0.0.0.0")
