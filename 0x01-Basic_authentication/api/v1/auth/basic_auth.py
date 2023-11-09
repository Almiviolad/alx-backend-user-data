#!/usr/bin/env python3
"""contains basic authn class"""
from api.v1.auth.auth import Auth


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
