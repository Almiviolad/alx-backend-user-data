#!/usr/bin/env python3
"""contains basic authn class"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic authetication class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header
for a Basic Authentication:"""
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        str_list = authorization_header.split()
        if str_list[0] != 'Basic':
            return None
        return str_list[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """returns the decoded value of a Base64
string base64_authorization_header"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            decoded_val = base64.b64decode(base64_authorization_header)
        except Exception:
            return None
        return decoded_val.decode('utf-8')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """returns the user email and password from
 the Base64 decoded value."""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email, pwd = decoded_base64_authorization_header.split(':')
        return (email, pwd)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password."""
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """_summary_
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(
                            email, password)

        return
