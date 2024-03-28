#!/usr/bin/env python3
"""flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """route handler for root endpoint"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users() -> str:
    """registers users"""
    data = request.form
    email = data.get('email')
    password = data.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login() -> str:
    """logs user in"""
    data = request.form
    email = data.get('email')
    password = data.get('password')
    if AUTH.valid_login(email, password):
        sess_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", sess_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """logout"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")



@app.route("/profile", methods=["GET"])
def profile() -> str:
    """Profile route"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
