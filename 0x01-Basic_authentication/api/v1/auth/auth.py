#!/usr/bin/env python3
"""Auth Class"""
from flask import request


class Auth():
    """basic auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth function"""
        return False
    def authorization_header(self, request=None) -> str:
        """authorization header function"""
        return None
    def current_user(self, request=None) -> TypeVar('User'):
        """returns current user"""
        return None
