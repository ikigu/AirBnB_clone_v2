#!/usr/bin/python3
""" Place Module for HBNB project """

import os
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """

    if os.environ['HBNB_TYPE_STORAGE'] == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)
        reviews = relationship('Review', backref='Place', cascade='delete')
        place_amenity = Table('place_amenity', Base.metadata,
                              Column('place_id', String(60),
                                     ForeignKey('places.id'),
                                     nullable=False)),
        Column('amenity_id', String(60), ForeignKey(
            'amenities.id'), nullable=False)
        user = relationship("User", back_populates="places")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            all_objects = models.storage.all()
            filtered_objects = {}

            for k, v in all_objects.items():
                if 'Review' in k:
                    filtered_objects[k] = v

            return filtered_objects

    def __init__(self, *args, **kwargs):
        """
        Initializes an instance of Place

        Args:
            self: instance of Place
            args: positional arguments
            kwargs: keyword arguments
        """
        super().__init__(*args, **kwargs)
