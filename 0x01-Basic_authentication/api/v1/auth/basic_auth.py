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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns decoded value of Base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            string = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(string)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """returns user credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        flag = false
        for char in decoded_base64_authorization_header:
            if char != ":":
                flag = true
        if flag == false:
            return None, None
        return decoded_base64_authorization_header.split(":")
