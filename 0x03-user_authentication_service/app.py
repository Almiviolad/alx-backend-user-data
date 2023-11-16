#!/usr/bin/env python3
"""flask app"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'])
def home() -> jsonify:
    """use flask.jsonify to return a JSON payload"""
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


@app.route("/users", methods=['POST'])
def register_user() -> str:
    """register a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        data = {"email": user.email, "message": "user created"}
        return jsonify(data)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """log a yser in and creates session"""
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)
    if not valid_login:
        return abort(401)
    else:
        session_id = AUTH.create_session(email)
    response = jsonify({"email": "<user email>", "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """destry session and log user out"""
    session_id = str(request.cookies.get('session_id'))
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('home'))
    else:
        return abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """returns emal.of user if user exist"""
    session_id = str(request.cookies.get('session_id'))
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """generate a token and respond with a 200 HTTP status 
and the following JSON payload:"""
    email = request.form.get('email')
    try:
        token = Auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
