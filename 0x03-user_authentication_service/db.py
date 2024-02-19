#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Add user to database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Find user by some crtain criteria

        Args:
            session (Session): db session object
            **kwargs: criteria to filter by

        Returns:
            User: first user that meets the criteria

        Raises:
            InvalidRequestError: Description
            NoResultFound: Description
        """
        for k in kwargs.keys():
            if k not in User.__dict__.keys():
                raise InvalidRequestError
        query = self._session.query(User).filter_by(**kwargs)
        # get the first row of user
        user = query.first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Update a User

        Args:
            user_id (int): User ID
            **kwargs: user attrs and value

        Returns:
            None: None

        Raises:
            ValueError: Description
        """
        for k in kwargs.keys():
            if k not in User.__dict__.keys():
                raise ValueError
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            setattr(user, k, v)
        self.__session.commit()

        return None