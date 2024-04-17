#!/usr/bin/python3
""" State Module for HBNB project """

from models import storage
from models.base_model import Base, BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    # Todo: For DBStorage
    cities = relationship("City", back_populates="parent",
                          cascade="all, delete", passive_deletes=True)

    # Todo: For FileStorage - should be private attribute
    @property
    def cities(self):
        all_objects = storage.all()

        all_cities = []

        for k, v in all_objects.items():
            if all_objects[k].state_id == self.id:
                all_cities.append(all_objects[k])
