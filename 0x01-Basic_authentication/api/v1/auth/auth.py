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
        for i in excluded_paths:
            if path.rstrip('/') == excluded_path.rstrip('/'):
                return False
            if path.startswith(excluded_path.rstrip('/') + '/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header function"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns current user"""
        return None
