from flask import Flask, jsonify, request
import sqlite3
import requests

app = Flask(__name__)
app.config["DEBUG"] = True

root_path = "http://127.0.0.1:5000"


@app.route('/', methods=['GET'])
def get_params():
    response = request.get_json()
    return jsonify({'test': 1})


app.run()


