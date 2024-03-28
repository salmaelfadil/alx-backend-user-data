#!/usr/bin/env python3
"""Authentican"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """hashes password"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt)


def _generate_uuid() -> str:
    """Generates a UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hash = _hash_password(password)
            user = self._db.add_user(email, hash)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """valudates login"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode("utf-8"),
                                      user.hashed_password)
        except Exception:
            return False

    def create_session(self, email) -> str:
        """creates session"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """returns user based on session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """destroys session"""
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """resets password"""
        try:
            user = self._db.find_user_by(email=email)
            id = _generate_uuid()
            self._db.update_user(user.id, reset_token=id)
        except Exception:
            raise ValueError()
        return id
