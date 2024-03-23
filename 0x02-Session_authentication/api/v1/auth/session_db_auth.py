#!/usr/bin/env python3
"""Authentication with Database"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """session database authentication"""
    def create_session(self, user_id=None):
        """creates session"""
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the user_id for the session"""
        if session_id is None:
            return None
        try:
            user_session = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if user_session[0].created_at + \
                timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return user_session[0].user_id

    def destroy_session(self, request=None) -> bool:
        """destroys session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        user_session = UserSession.search(
            {'session_id': session_id, 'user_id': user_id})
        if user_session is None:
            return False

        user_session[0].delete()
        return True
