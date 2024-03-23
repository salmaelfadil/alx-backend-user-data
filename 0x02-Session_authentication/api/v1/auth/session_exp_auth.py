#!/usr/bin/env python3
"""Session Authentication with expirtation"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """session expiration class"""
    def __init__(self):
        """initialization method"""
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """creates session method"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns user_id for the current session"""
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        user_id = session_dict.get('user_id')
        if self.session_duration <= 0:
            return user_id
        created_time = session_dict.get('created_at')
        if created_time is None:
            return None
        if created_time + timedelta(seconds=self.session_duration) < \
           datetime.now():
            return None
        return user_id
