#!/usr/bin/python3
"""This module defines a class User"""

import os
from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey


class User(BaseModel):
    """This class defines a user by various attributes"""

    if os.environ['HBNB_TYPE_STORAGE'] == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128, nullable=True))
        last_name = Column(String(128, nullable=True))
    email = ''
    password = ''
    first_name = ''
    last_name = ''
