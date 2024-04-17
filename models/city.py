#!/usr/bin/python3
""" City Module for HBNB project """


from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship


class City(BaseModel, Base):
    """
    The city class, contains state ID and name
    """

    __tablename__ = 'cities'

    name = Column(String(128), nullabe=False)
    state_id = mapped_column(ForeignKey(
        "states.id", ondelete="CASCADE"), Column(60), nullable=False)
    state = relationship("State", back_populates="children")
