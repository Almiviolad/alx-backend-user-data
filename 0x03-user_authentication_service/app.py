#!/usr/bin/env python3
"""flask app"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=['GET'])
def home() -> jsonify:
    """use flask.jsonify to return a JSON payload"""
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
