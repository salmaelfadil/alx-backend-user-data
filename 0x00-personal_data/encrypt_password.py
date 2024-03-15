#!/usr/bin/env python3
"""Task 5 Module"""
import bcrypt


def hash_password(password: str) -> str:
    """hashes a password"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt)
