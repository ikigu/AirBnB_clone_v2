#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class Amenity(BaseModel, Base):
    """The amenity class"""

    if os.environ['HBNB_TYPE_STORAGE'] == 'db':
        __tablename__ = 'amenities'

        name = Column(String(128), nullable=False)
        place_amenities = ''  # Todo: create a many-to-many relationship
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """
        Initializes instance of Amenity class

        Args:
            self (Amenity object): represents instance of Amenity class
            args (tuple): positional arguments
            kwargs (dict): keyword arguments
        """
        super().__init__(*args, **kwargs)
