#!/usr/bin/python3
"""User file for views module"""
from api.v1.views import app_views
from flask import jsonify, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.app import handle_err


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def places(city_id):
    """ This method request for places. """
    city_needed = storage.get(City, city_id)
    if city_needed:
        return jsonify([item.to_dict() for item in city_needed.places])
    return handle_err('err')


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def places_id(place_id):
    """ This method filters the places by id. """
    obj = storage.get(Place, place_id)
    if obj:
        return jsonify(obj.to_dict())
    return handle_err('err')


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def placesDelete(place_id):
    """ This method deletes a place by id """
    obj = storage.get(Place, place_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    return handle_err('err')


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def placesPost(city_id):
    """ This method create a new object. """
    obj = storage.get(City, city_id)
    if not obj:
        return handle_err('err')
    try:
        req = request.get_json()
        if 'user_id' not in req:
            return "Missing user_id", 400
        idUser = storage.get(User, req["user_id"])
        if not idUser:
            return handle_err('err')
        if 'name' not in req:
            return "Missing name", 400
        new_obj = Place()
        setattr(new_obj, "city_id", city_id)
        for key, value in req.items():
            setattr(new_obj, key, value)
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201
    except:
        return "Not a JSON\n", 400


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def placesPut(place_id):
    """ This method update an object through http request """
    try:
        req = request.get_json()
        obj = storage.get(Place, place_id)
        if obj:
            for key, value in req.items():
                setattr(obj, key, value)
            storage.save()
            return jsonify(obj.to_dict()), 200
        return handle_err('err')
    except:
        return "Not a JSON\n", 400
