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
    response = request.get_json()
    return jsonify(response)


app.run(host="0.0.0.0")
