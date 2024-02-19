#!/usr/bin/env python3
""" Simple flask app
"""

from flask import (Flask, jsonify, request, abort, redirect)
from auth import Auth

app: Flask = Flask(__name__)

AUTH: Auth = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home() -> dict:
    """ / endpoint

    Returns:
        dict: json object
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user() -> dict:
    """ Register user endpoint

    Returns:
        dict: json response
    """
    # get the json payload data
    data = request.form
    email = data['email']
    passwd = data['password']
    try:
        user = AUTH.register_user(email, passwd)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{email}", "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> dict:
    """ Login user and create a session
    """
    data = request.form
    email = data['email']
    passwd = data['password']
    if AUTH.valid_login(email, passwd):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> dict:
    """ Logout user session
    """
    session_id = request.cookies.get("session_id", None)
    # get user from session id
    user = AUTH.get_user_from_session_id(session_id)
    if not user or session_id is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> dict:
    """ Logout user session
    """
    session_id = request.cookies.get("session_id", None)
    # get user from session id
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> dict:
    """ Get password reset token
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": f"{email}", "reset_token": f"{reset_token}"})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> dict:
    """ Update password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, password)
    except ValueError:
        abort(403)
    return jsonify({"email": f"{email}", "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)