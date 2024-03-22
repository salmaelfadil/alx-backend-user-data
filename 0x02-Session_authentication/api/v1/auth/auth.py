#!/usr/bin/env python3
"""Auth Class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """basic auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth function"""
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False
        for i in excluded_paths:
            if i.startswith(path):
                return False
            elif path.startswith(i):
                return False
            elif i[-1] == "*":
                if path.startswith(i[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header function"""
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """returns current user"""
        return None

    def session_cookie(self, request=None):
        """returns cookie value from request"""
        if request is None:
            return None
        cookie_name = current_app.config.get(
            'SESSION_NAME', '_my_session_id')
        return request.cookies.get(cookie_name)
