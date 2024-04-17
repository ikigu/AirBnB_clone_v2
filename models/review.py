#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class Review(BaseModel, Base):
    """ Review class to store review information """

    if os.environ['HBNB_TYPE_STORAGE'] == 'db':
        __tablename__ = 'reviews'

        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """
        Initializes a Review instance

        Args:
            self: instance of Review
            args: positional arguments
            kwargs: key-word arguments
        """

        super().__init__(self, args, kwargs)
