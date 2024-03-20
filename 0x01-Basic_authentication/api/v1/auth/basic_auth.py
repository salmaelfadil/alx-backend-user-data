#!/usr/bin/env python3
"""Basic Auth Class"""
from .auth import Auth
import base64


class BasicAuth(Auth):
    """Basic Auth Class"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """returns the Base64 encoding of the header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[-1]
