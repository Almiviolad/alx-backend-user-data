#!/usr/bin/env python3
"""auth file"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """that takes in a password string arguments
and returns bytes.

The returned bytes is a salted hash of the input password,
hashed with bcrypt.hashpw."""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    new_uuid = uuid.uuid4()
    return str(new_uuid)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """take mandatory email and password string
arguments and return a User object."""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        else:
            raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """validaes email and password"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """takes an email string argument
and returns the session ID as a string."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[None, User]:
        """gets user usng sessiin id"""
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """updates the corresponding user’s session ID to None."""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except Exception as e:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Find the user corresponding to the email.
If the user doebs not exist, raise a ValueError exception.
If it exists, generate a UUID and update the user’s
reset_token database field. Return the token."""
        try:
            user = self._db.find_user_by(email=email)
            token = str(uuid.uuid4())
            self._db.update_user(user.id, reset_token=token)
            return user.reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """_summary_

        Args:
            reset_token (str): _description_
            password (str): _description_
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        else:
            user.hashed_password = _hash_password(password)
            user.reset_token = None
            return None
