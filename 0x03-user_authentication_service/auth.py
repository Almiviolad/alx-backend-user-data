#!/usr/bin/env python3
"""auth file"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """that takes in a password string arguments
and returns bytes.

The returned bytes is a salted hash of the input password,
hashed with bcrypt.hashpw."""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password
