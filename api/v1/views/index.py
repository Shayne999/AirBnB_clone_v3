#!/usr/bin/python3

""" creates a route /status on the object app_views """

import models
from models import storage
from models.base_model import BaseModel
from flask import jsonify
from api.v1.views import app_views

@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """ Returns a JSON with status "OK" """
    return jsonify({"status": "OK"}), 200

@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """ Returns a JSON response with the count of various objects
    """
    data = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User"),
    }

    return jsonify(data), 200
