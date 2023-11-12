#!/usr/bin/env python3
"""contains basic authn class"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session authetication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a new session"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        self.session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[
            self.session_id] = user_id
        return self.session_id
