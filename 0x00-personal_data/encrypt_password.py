#!/usr/bin/env python3
"""Task 5 Module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hashes a password"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validates if the provided pass matches the hashed pass"""
    return bcrypt.checkpw(password.encode(), hashed_password)
