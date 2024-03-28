#!/usr/bin/env python3
"""flask app"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """route handler for root endpoint"""
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=['POST'])
def users():
    """registers users"""
    data = request.form
    email = data.get('email')
    password = data.get('password')
    try:
        Auth.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
