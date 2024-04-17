#!/usr/bin/python3

"""
Sets up Database Storage for HBNB
"""


from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker
import os

HBNB_MYSQL_USER = os.environ['HBNB_MYSQL_USER']
HBNB_MYSQL_PWD = os.environ['HBNB_MYSQL_PWD']
HBNB_MYSQL_HOST = os.environ['HBNB_MYSQL_HOST']
HBNB_MYSQL_DB = os.environ['HBNB_MYSQL_DB']
HBNB_ENV = os.environ['HBNB_ENV']


class DBStorage():
    """
    Sets up DBStorage
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the database engine

        Args:
            self: represents instance of DBStorage
        """

        sql_db = {
            'drivername': 'mysql+mysqldb',
            'host': HBNB_MYSQL_HOST,
            'username': HBNB_MYSQL_USER,
            'password': HBNB_MYSQL_PWD,
            'database': HBNB_MYSQL_DB,
        }

        self.__engine = create_engine(URL.create(**sql_db), pool_pre_ping=True)

        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries the database for all objects of cls.
        If cls is none, returns all objects.

        Args:
            self: instance of DBStorage object
            cls: The specific class to query objects of
        """

        all_objects = {}

        if cls is not None:
            if type(cls) is str:
                cls = eval(cls)

            filtered_objects = self.__session.query(cls).all()

            if filtered_objects is not None:
                for obj in filtered_objects:
                    object_key = obj.__class__ + '.' + obj.id

                    all_objects[object_key] = obj
        else:
            amenities = self.__session.query(Amenity).all()
            cities = self.__session.query(City).all()
            places = self.__session.query(Place).all()
            reviews = self.__session.query(Review).all()
            states = self.__session.query(State).all()
            users = self.__session.query(User).all()

            queried_objs = [amenities, cities, places, reviews, states, users]

            for objects in queried_objs:
                if objects is not None:
                    for obj in objects:
                        object_key = obj.__class__ + '.' + obj.id

                        all_objects[object_key] = obj

        return all_objects

    def new(self, obj):
        """
        Adds obj to the current database session

        Args:
            self: represents instance of the class
            obj: object to add to the database
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current databse session

        Args:
            self: represents instance of the class
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete, from the current database session, obj if not None

        Args:
            self: represents instance of the class
            obj: the object to delete from the session
        """
        self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
