#!/usr/bin/env python3
""" Auth Module
"""


from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register User

        Args:
            email (str): user's email
            password (str): user's password

        Returns:
            User: registered user

        Raises:
            ValueError: if User exists
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Check if password is correct to validate login

        Args:
            email (str): User email
            password (str): User password
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        password = password.encode('utf-8')
        if checkpw(password, user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        """ create a session

        Args:
            email (str): user's email

        Returns:
            str: session id or none if user doesn't exist
        """
        try:
            user = self._db.find_user_by(email=email)
            uid = _generate_uuid()
            setattr(user, "session_id", uid)
            self._db._session.commit()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ get user from session id

        Args:
            session_id (str): user session id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """ Destroy user session

        Args:
            user_id (int): User Id

        Returns:
            None: None
        """
        # get the user by user_id
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ Get rese password toke

        Args:
            email (str): User's email
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Update passord

        Args:
            reset_token (str): password reset token
            password (str): password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(
            user.id, hashed_password=hashed_password, reset_token=None)
        return None


def _generate_uuid() -> str:
    """ Generate unique identifier
    """
    return str(uuid4())


def _hash_password(password: str) -> bytes:
    """ Hash Pasword

    Args:
        password (str): password to be hashed

    Returns:
        bytes: hashed result
    """
    passwd = password.encode('utf-8')
    return hashpw(passwd, gensalt())