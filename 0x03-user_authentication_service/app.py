#!/usr/bin/env python3
"""flask app"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)


@app.route("/", methods=['GET'])
def home() -> jsonify:
    """use flask.jsonify to return a JSON payload"""
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


@app.route("/users", methods=['POST'])
def register_user() -> jsonify:
    """register a user"""
    auth = Auth()
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = auth.register_user(user.email, password)
        data = {"email": email, "message": "user created"}
        return jsonify(data)
    except Exception:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
