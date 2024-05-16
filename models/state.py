#!/usr/bin/python3
""" State Module for HBNB project """

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
import os
import models


class State(BaseModel, Base):
    """ State class """

    if os.environ['HBNB_TYPE_STORAGE'] == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        # cities = relationship(
        #     "City", cascade="all, delete-orphan", back_populates="states")
    else:
        name = ""

        @property
        def cities(self):
            """FileStorage cities getter attribute"""
            all_objects = models.storage.all()

            all_cities = []

            for k, v in all_objects.items():
                try:
                    if all_objects[k].state_id == self.id:
                        all_cities.append(all_objects[k])
                except AttributeError:
                    pass

            return all_cities

    def __init__(self, *args, **kwargs):
        """Initialize State"""
        super().__init__(*args, **kwargs)
