#!/usr/bin/python

"""
This is a learning module.
"""

# SQLALchemy ORM

# User-defined classes                 -> Database Tables
# Instances of these classes (objects) -> Row of the database tables

# Changes in state between objects and their related rows
# are synchronized (automatically?) by a system that's included.

from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# When using ORMs, the config process starts be describing the database tables
# we'll be dealing with and then defining our own classes that will be mapped
# to those tables. Both these things are dong using Declarative.

# Declarative seems to be the one that does the mapping????

# Classes mapped using the Declarative system are defined in terms
# of a base class which maintains a catalogue of classes and tables
# relative to that base in a commonly imported module.
# The declarative_base() function creates the Base class.

Base = declarative_base()

# The echo flag sets up SQLAlchemy logging. We'll see the generated SQL this way.
# create_engine() returns an instance of Engine, which is the core interface
# to the database.

# Calling Engine.execute() or Engine.connect() establishes
# a real DBAPI connection to the database, which is used to emit SQL.
# With the ORM, we won't interact with the Engine directly.

# This code will make it easier to create an engine

"""
>>> from sqlalchemy.engine.url import URL
>>> from sys import argv

>>> sql_db = {
...    'drivername': 'mysql+mysqldb',
...    'host': 'localhost',
...    'port': 3306,
...    'username': argv[1],
...    'password': argv[2],
...    'database': argv[3]
... }

>>> engine = create_engine(URL.create(**sql_db))
"""

engine = create_engine('mysql://ikigu:h1t quan@localhost/sqlalchemy')

# engine = create_engine('sqlite:///:memory:', echo=False)

# Session is the ORM's handle to the database. It lets us talk to the database.
Session = sessionmaker(bind=engine)


# User is a mapped class based on Base. It maps to a table called 'users'.
# SQLAlchemy uses a Table object to represent the information about the
# class we've created.

class User(Base):
    __tablename__ = 'users'

    # Sequence is required by Oracle for sth??
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

    def __repr__(self):
        return f'<User(name={self.name}, fullname={self.fullname}, nickname={self.nickname})>'


# When User class was created, Declarative did additional operations,
# it created a Table object according to our specs,
# and associated it with the class by constructing a Mapper object.
# The Table object is a member of a larger collection: MetaData, a registry
# that includes the ability to emit a limited set of schema generation
# commands to the database.

# Using the metadata to create the tables, if they don't exist
Base.metadata.create_all(engine)

# create a new user
ed_user = User(name='ed', fullname='Ed Jones', nickname='EJ')

# Whenever you need to have a conversation with the database,
# instantiate a Session
session = Session()

# To persist a user object
session.add(ed_user)

# At this stage, the instance is pending, no SQL has been issued.
# The object is not yet represented by a row in the database.
# Session will issue SQL to persist Ed Jones as soon as is needed,
# using a process known as a flush.

# If we query the database for Ed Jones, all pending information
# will be first flushed, and the query is issued immediately thereafer.

our_user = session.query(User).filter_by(name='ed').first()

# ed_user is our_user will return True.
# Session identifies that the row returned is the same row
# as one already represented within its internal map of objects.
# So we get back the identical instance as that which
# we just added.

# You can add more User objects at once using add_all(), these will be pending
session.add_all([
    User(name='wendy', fullname='Wendy Williams', nickname='windy'),
    User(name='mary', fullname='Mary Contrary', nickname='mary'),
    User(name='fred', fullname='Fred Flintstone', nickname='freddy')])


# Let's update Ed's nickname
ed_user.nickname = 'eddie'

# The Session will know that Ed Jones has been modified:

# >>> session.dirty
# IdentitySet([<User(name='ed', fullname='Ed Jones', nickname='eddie')>])


# To insert Wendy, Mary and Fred and update Eddie (pending changes), run session.commit()
session.commit()

# This will also now give all new Users ids
# ed_user.id will be 1

for instance in session.query(User).order_by(User.id):
    print(instance.name, instance.fullname, instance.nickname)
