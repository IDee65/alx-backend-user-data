#!/usr/bin/env python3
""" encrypts password """

import bcrypt
from bcrypt import hashpw, checkpw


def hash_password(password: str) -> bytes:
    """ Hash password function

    Args:
        password (str): password to encrypt

    Returns:
        str: encrypted password
    """
    # encode password
    encoded_pssw: bytes = password.encode()
    encrypted: bytes = hashpw(encoded_pssw, bcrypt.gensalt())
    return encrypted


def is_valid(hashed_pssw: bytes, password: str) -> bool:
    """ checks if password is encrypted

    Args:
        hashed_pssw (bytes): hashed password
        password (str): password

    Returns:
        bool: true or false
    """
    return checkpw(password.encode(), hashed_pssw)
