#!/usr/bin/python3

"""
Starts a Flask web application
"""

from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def hello_hbnb():
    """Root path"""
    return "Hello HBNB!"


@app.route("/hbnb")
def hbnb():
    """hbnb path"""
    return "HBNB"


@app.route("/c/<text>")
def c_text(text):
    """c text path"""
    return f"C {escape(text).replace('_', ' ')}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
