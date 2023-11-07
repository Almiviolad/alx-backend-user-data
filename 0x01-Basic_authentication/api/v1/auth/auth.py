#!/usr/bin/env python3
"""contains auth class"""
from flask import request
from typing import List, TypeVar


class Auth():
    """class to manage the API authentication"""

    def require_auth(self,
                     path: str,
                     excluded_paths: List[str]) -> bool:
        """require auth method"""
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path = path + '/'
        if path not in excluded_paths:
            return True

        return False

    def authorization_header(self, request=None) -> str:
        """authorization_header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ currnt user"""
        return None
