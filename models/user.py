#!/usr/bin/python3
"""This module defines a class User"""

import os
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This class defines a user by various attributes"""

    if os.environ['HBNB_TYPE_STORAGE'] == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship('Place', backref='User', cascade='delete')
        reviews = relationship('Review', backref='User', cascade='delete')

    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''

    def __init__(self, *args, **kwargs):
        """
        Initialize user

        Args:
            self: represents instance of User object
            args: positional arguments
            kwargs: key-word arguments
        """
        super().__init__(*args, **kwargs)
