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

try:
    HBNB_ENV = os.environ['HBNB_ENV']
except KeyError:
    HBNB_ENV = None


class DBStorage:
    """
    Sets up DBStorage
    """

    __classes = {
        'Amenity': Amenity,
        'City': City,
        'Place': Place,
        'Review': Review,
        'State': State,
        'User': User,
    }

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

        if self.__session is None:
            self.reload()

        all_objects = {}

        if cls is not None:
            if type(cls) is str:
                cls = eval(cls)

            filtered_objects = self.__session.query(cls).all()

            if filtered_objects is not None:
                for obj in filtered_objects:
                    object_key = obj.__class__.__name__ + '.' + obj.id

                    all_objects[object_key] = obj
        else:
            for k, v in self.__classes.items():
                for obj in self.__session.query(self.__classes[k]):
                    all_objects[obj.__class__.__name__ + '.' + obj.id] = obj

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
        Creates all tables in the database

        Args:
            self: represents instance of the class
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """
        Closes the storage
        """

        self.__session.remove()
