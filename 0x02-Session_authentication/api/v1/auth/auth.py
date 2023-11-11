#!/usr/bin/env python3
"""contains auth class"""
from flask import request
from typing import List, TypeVar
import re


class Auth():
    """class to manage the API authentication"""

    def require_auth(self,
                     path: str,
                     excluded_paths: List[str]) -> bool:
        """require auth method"""
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path = path + '/'
        for e_path in excluded_paths:
            match = re.match(e_path, path)
            if match:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization_header"""
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """ currnt user"""
        return None
