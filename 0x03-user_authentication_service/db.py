#!/usr/bin/env python3
"""DB module"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy import inspect
from user import Base, User
from typing import Dict
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class"""
    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add user method"""
        row = User(email=email, hashed_password=hashed_password)
        self._session.add(row)
        self._session.commit()
        return row

    def find_user_by(self, **kwargs: Dict) -> int:
        """Searches for users in db"""
        query = self._session.query(User)
        for key, value in kwargs.items():
            if hasattr(User, key):
                query = query.filter(getattr(User, key) == value)
            else:
                raise InvalidRequestError()
        if query.first() is None:
            raise NoResultFound()
        return query.first()

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """updates user"""
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(User, key):
                setattr(user, key, value)
            else:
                raise ValueError()
        self._session.commit()
