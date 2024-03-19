#!/usr/bin/env python3
"""Auth Class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """basic auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth function"""
        if path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header function"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns current user"""
        return None
