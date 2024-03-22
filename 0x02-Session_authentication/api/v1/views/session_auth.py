#!/usr/bin/env python3
"""routes for Session authentication."""
from flask import abort, jsonify, request
from api.v1.auth.session_auth import SessionAuth
from models.user import User
from api.v1.views import app_views
from os import getenv
from typing import Tuple

auth = SessionAuth()

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """login method"""
    email = request.form.get('email')
    if not email:
        return jsonify({ "error": "email missing" }), 400
    password = request.form.get('password')
    if not password:
        return jsonify({ "error": "password missing" }), 400
    try:
        users = User.search({'email': email})
        if not users or users == []:
            return jsonify({ "error": "no user found for this email" }), 404
        for user in users:
            if user.is_valid_password(password):
                user_id = user.id
                from api.v1.app import auth
                session_id = auth.create_session(user_id)
                res = jsonify(user.to_json())
                response.set_cookie(getenv('SESSION_NAME'), session_id)
                return res
            else:
                return jsonify({ "error": "wrong password" }), 401
    except Exception:
        return
