#!/usr/bin/env python3
"""Authentican"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hashes password"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt)
