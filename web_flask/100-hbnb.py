#!/usr/bin/python3

"""
Write a script that starts a Flask web application

Requirements:
    - Your web application must be listening on 0.0.0.0, port 5000
    - You must use storage for fetching data
      from the storage engine(FileStorage or DBStorage) = >
        from models import storage and storage.all(...)
    - To load all cities of a State:
        - If your storage engine is DBStorage, you must use cities relationship
        - Otherwise, use the public getter method cities
    - After each request you must remove the current SQLAlchemy Session:
        - Declare a method to handle @app.teardown_appcontext
        - Call in this method storage.close()
"""

from flask import Flask
from flask import render_template
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def close(self):
    """Destroys SQLAlchemy session"""
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb_filters():
    """Renders a page with all states and their corresponding cities"""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    places = storage.all("Place")

    return render_template('100-hbnb.html',
                           states=states, amenities=amenities,
                           places=places)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
